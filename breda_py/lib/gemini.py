from google.genai import types
from .gemini_client import GeminiClient
from typing import List
import json
from PIL import Image
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or ""

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY no està configurat a les variables d'entorn.")

class Gemini:
    def __init__(self, img:List[str]):
        self.img=img

    def get_result(self):

        image = Image.open(f"uploaded_files/{self.img[0]}")
        try:
            model = "gemini-flash-latest"
            system_prompt = """
                Eres un asistente experto en análisis documental y extracción estructurada de datos.
                Tu tarea es interpretar facturas (en imagen o texto OCR) y devolver los datos principales
                de forma precisa y estandarizada en formato JSON.

                Además, debes inferir el tipo de material o gasto de la factura en base al contenido,
                descripciones de productos o naturaleza del proveedor.

                Reglas:
                - No incluyas texto fuera del JSON.
                - Si un dato no aparece, deja el campo vacío ("").
                - Clasifica el tipo de material en una de estas categorías:
                ["comida", "bebidas", "menaje", "limpieza", "servicios", "suministros", "otros"].
                - Usa sentido común y el nombre del proveedor o productos para inferir la categoría.
                - Estandariza los valores numéricos a dos decimales (con punto decimal).
                - Si hay varias facturas, devuelve una lista JSON con cada una como objeto independiente.
                """

            user_prompt = """
                Analiza las siguientes imágenes de facturas y devuelve, en formato JSON, los campos:
                num de documento, fecha, proveedor,NIF o CIF, tipo_material, total.
                """
            gemini = GeminiClient()

            response = gemini.client.models.generate_content(
                model=model,
                contents=[system_prompt, user_prompt, image],
            )
            raw_text = response.candidates[0].content.parts[0].text
            clean_text = raw_text.strip("```").replace("json", "").strip()

            try:
                data = json.loads(clean_text)
                return data
            except json.JSONDecodeError:
                print("⚠️ No se pudo parsear el JSON, texto crudo:")

        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
