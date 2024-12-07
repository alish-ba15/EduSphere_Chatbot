from fpdf import FPDF
import json
from io import BytesIO


class QuizPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Generated Quiz', ln=True)
        self.ln(5)

    def add_question(self, number, question, options):
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f"{number}. {question}", ln=True)
        self.set_font('Arial', '', 11)
        for key, value in options.items():
            self.cell(0, 10, f"{key}: {value}", ln=True)
        self.ln(3)


json_file_path = "quiz_response.json"


def load_quiz_data(json_file_path):
    """
    Loads quiz data from a saved JSON file.
    
    Args:
        json_file_path (str): Path to JSON data file.
    
    Returns:
        dict: Dictionary containing quiz data.
    """
    with open(json_file_path, 'r') as file:
        return json.load(file)

