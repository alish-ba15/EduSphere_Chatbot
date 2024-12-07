import PyPDF2
import json
import traceback


def parse_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except PyPDF2.utils.PdfReadError:
            raise Exception("Error reading the PDF file.")

    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        raise Exception(
            "Unsupported file format. Only PDF and TXT files are supported."
        )


def get_table_data(quiz_str):
    try:
        # Convert the quiz from a string to a dictionary
        if "### RESPONSE_JSON" in quiz_str:
            quiz_str = quiz_str.replace("### RESPONSE_JSON", "").strip()
        print("Raw quiz_str:", quiz_str)
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        # Iterate over the quiz dictionary and extract the required information
        for key, value in quiz_dict.items():
            # Safely access expected keys
            mcq = value.get("mcq", "No question provided")
            options = value.get("options", {})
            correct = value.get("correct", "No correct answer provided")

            # Ensure options is a dictionary
            
            if isinstance(options, dict):
                options_str = "    |    ".join(
                    [f"{option}: {option_value}" for option, option_value in options.items()]
                )
            else:
                options_str = "No options available"

            # Append extracted data to the quiz table
            quiz_table_data.append({"MCQ": mcq, "Choices": options_str, "Correct": correct})

        return quiz_table_data

    except json.JSONDecodeError as e:
        print("JSONDecodeError: Invalid JSON string provided.", e)
        return None
    except KeyError as e:
        print(f"KeyError: Missing key in quiz data - {e}")
        return None
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return None



RESPONSE_JSON = {
    "1": {
        "no": "1",
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "2": {
        "no": "2",
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "3": {
        "no": "3",
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
}