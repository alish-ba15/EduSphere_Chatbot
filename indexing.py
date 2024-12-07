import os
import json
from dotenv import load_dotenv
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
from langchain.schema import Document  # Import Document class
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()

# Folder path and output file
AUDIO_FOLDER = "YouTube_Audio"  # Path to audio folder
OUTPUT_JSON_FILE = "Output.json"  # File to store all results
CHROMADB_DIRECTORY = "./Chroma_Indexing_db"  # Directory for ChromaDB

def transcribe_audio(audio_file, client):
    """Transcribe a single audio file and return the response."""
    try:
        with open(audio_file, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        # Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        # Transcribe the file
        response = client.listen.rest.v("1").transcribe_file(payload, options)

        return response.to_json(indent=4)

    except Exception as e:
        print(f"Error transcribing {audio_file}: {e}")
        return None

def index_transcriptions_to_chromadb(documents):
    """Index the transcriptions into ChromaDB."""
    try:
        # Initialize text splitter
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

        # Split documents into chunks
        split_docs = splitter.split_documents(documents)

        # Initialize embeddings and ChromaDB
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        db = Chroma(
            collection_name="doc_splitter",
            embedding_function=embeddings,
            persist_directory=CHROMADB_DIRECTORY,
        )

        # Add documents to the database
        resp = db.add_documents(split_docs)
        print(f"Documents added successfully to ChromaDB: {resp}")

    except Exception as e:
        print(f"Error indexing documents to ChromaDB: {e}")

def main():
    try:
        # STEP 1: Create a Deepgram client using the API key
        deepgram = DeepgramClient()

        # Initialize list to store all processed data
        all_transcriptions = []
        lecture_number = 1

        # Iterate through all audio files in the folder
        for filename in os.listdir(AUDIO_FOLDER):
            if filename.endswith(".mp3") or filename.endswith(".wav"):  # Adjust based on your file types
                audio_path = os.path.join(AUDIO_FOLDER, filename)

                # Transcribe the audio file
                response_data = transcribe_audio(audio_path, deepgram)

                if response_data:
                    # Process the transcription
                    data = json.loads(response_data)
                    transcription = (
                        data.get("results", {})
                        .get("channels", [{}])[0]
                        .get("alternatives", [{}])[0]
                        .get("transcript", "")
                    )

                    request_id = data.get("metadata", {}).get("request_id", "")
                    duration = data.get("metadata", {}).get("duration", 0)

                    if transcription.strip():  
                        print(f"\nLecture : {lecture_number} : {transcription}")

                        # Create result entry for this transcription
                        result_data = {
                            "lecture_number": lecture_number,
                            "request_id": request_id,
                            "duration": duration,
                            "transcript": transcription,
                        }

                        # Add to the list of all transcriptions
                        all_transcriptions.append(result_data)

                        lecture_number += 1

        # Save all transcriptions to a single JSON file
        with open(OUTPUT_JSON_FILE, "w") as output_json_file:
            json.dump(all_transcriptions, output_json_file, indent=4)

        # Prepare documents for ChromaDB
        chromadb_documents = [
            Document(page_content=transcription["transcript"], metadata={
                "request_id": transcription["request_id"],
                "duration": transcription["duration"]
            })
            for transcription in all_transcriptions
        ]

        # Index transcriptions into ChromaDB
        if chromadb_documents:
            index_transcriptions_to_chromadb(chromadb_documents)
        else:
            print("No transcriptions to index into ChromaDB.")

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()