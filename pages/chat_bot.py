import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import os
import json
import logging

# Configure logging
# logging.basicConfig(level=logging.INFO)

CHROMADB_DIRECTORY = "./Chroma_Indexing_db"  # Directory for ChromaDB
load_dotenv()

# --- Initialize LLM and Embeddings (outside main function) ---
try:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    llm = GoogleGenerativeAI(model="gemini-pro")
except Exception as e:
    st.error(f"Error initializing LLM or embeddings: {e}")
    st.stop()

# --- Initialize ChromaDB (outside main function) ---
try:
    db = Chroma(
        collection_name="doc_splitter",
        embedding_function=embeddings,
        persist_directory=CHROMADB_DIRECTORY,
    )
    print("Done")
    retriver = db.as_retriever()
except Exception as e:
    st.error(f"Error initializing ChromaDB: {e}")
    st.stop()

prompt = ChatPromptTemplate.from_template("""
You are an intelligent assistant designed to answer questions based only on the content of a specific video. The video has been transcribed, and the transcription is stored in a database. When a user asks a question, your task is to retrieve the most relevant information from the video transcription to provide an accurate and concise answer. If a question cannot be answered based on the video's content, politely inform the user. Do not provide information outside the scope of the video's transcription.
Understand the query in detail and match it with the relevant parts of the video transcription.
Avoid speculating or answering with content not found in the transcription.
If user ask for topics in lecture give the topics from the transcription.                                                                                                                                
Provide clear, concise answers based solely on the transcribed video.\n\n
    Context:\n {context}?\n
Question : {input}""")


chain = create_stuff_documents_chain(llm, prompt)
retrievel_chain = create_retrieval_chain(retriver, chain)


def process_user_input(user_input):
    """Processes user input and returns the chatbot's response."""
    try:
        response = retrievel_chain.invoke({"input": user_input})
        print(response["answer"])
        return response["answer"]
    except Exception as e:
        logging.exception(e)
        return f"Error: {e}"
    
def load_lecture_data():
    with open("Output.json", "r") as file:
        data = json.load(file)  # Load the JSON file
    return data


def get_lecture_options():
    """Extract available lectures from JSON data."""
    data = load_lecture_data()
    lecture_options = {
        f"Lecture {item['lecture_number']}": item['transcript'] for item in data
    }
    return lecture_options


def main():
    st.sidebar.page_link("app.py", label="Switch accounts")

    st.sidebar.header("Lecture Selector")
    
    # Extract available lecture options
    lecture_options = get_lecture_options()
    selected_lecture = st.sidebar.selectbox("Select a Lecture", ["-- Select a Lecture --"] + list(lecture_options.keys()))

    # If no lecture is selected, don't show anything further
    if selected_lecture == "-- Select a Lecture --":
        st.info("Please select a lecture to proceed with the chatbot simulation.")
        return

    # Clear chatbot history and session state if the lecture is changed
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if st.session_state.get("selected_lecture") != selected_lecture:
        # Reset chat state & history when user selects a new lecture
        st.session_state.messages = []
        st.session_state.selected_lecture = selected_lecture

    # Display only the selected lecture's transcript
    st.subheader("Lecture Transcript")
    st.write(lecture_options[selected_lecture])

    # Simulate chatbot interaction
    st.subheader("Chatbot Simulation")
    
    # Render chat history if it exists
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input box for user question
    if user_query := st.chat_input("Ask a question"):
        st.session_state.messages.append({"role": "user", "content": user_query})

        # Show user query in the UI
        with st.chat_message("user"):
            st.markdown(user_query)

        # Generate chatbot response based on the currently selected lecture
        context_data = lecture_options.get(selected_lecture, "")
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            response = process_user_input(user_query)
            response_placeholder.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()