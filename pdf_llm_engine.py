import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
You are a helpful assistant for clinicians and operations staff.
You are given the text of a PDF that is related to insurance, prescriptions, and appeals.
Answer questions using only the information in the document.
If you cannot find the answer in the document, say you do not know.
Keep the responses very concise. For example, if you are asked "What is x", do not respond with "x is y...", just respond with "y". 
If it is a yes/no question, respond with only one word, either "yes" or "no". Do not add punctuation or any other details.
Do not use acronyms by themselves. Write what it stands for and the acronym in parenthesis.
""".strip()


class PdfLLMEngine:
    """Uses GPT-5.1 to answer questions about PDF content."""
    
    def __init__(self, model="gpt-5.1"):
        self.model = model
        self.document_text = ""

    def set_document(self, text):
        """Set the PDF text content for answering questions."""
        self.document_text = text

    def ask(self, question):
        """
        Ask a question about the document.
        
        Args:
            question: Question string
            
        Returns:
            Answer string from the LLM
        """
        if not self.document_text:
            raise ValueError("No document text has been set yet")

        input_items = [
            {
                "role": "system",
                "content": [
                    {"type": "input_text", "text": SYSTEM_PROMPT}
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Here is the document text:\n\n"
                            f"{self.document_text}\n\n"
                            f"Question: {question}"
                        ),
                    }
                ],
            },
        ]

        response = client.responses.create(
            model=self.model,
            input=input_items,
            reasoning={"effort": "low"},
            text={"verbosity": "medium"},
        )

        return response.output_text