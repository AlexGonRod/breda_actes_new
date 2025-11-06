import os
from google import genai
from google.genai.errors import APIError
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or ""

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY no està configurat a les variables d'entorn.")

class GeminiClient:
    def __init__(self):
        self.api_key=GEMINI_API_KEY

        try:
            self.client = genai.Client(api_key=self.api_key)
        except APIError as e:
            return f"Error connecting to Gemini API: {str(e)}"
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")







