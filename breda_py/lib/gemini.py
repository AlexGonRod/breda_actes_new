from google.genai import types
from .gemini_client import GeminiClient
from typing import List
import json
from PIL import Image

class Gemini:
    def __init__(self, imgs:List[str]):
        self.imgs=imgs
        self.data: list[dict] = []
        self.gemini = GeminiClient()

    def get_result(self):

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

        for image in self.imgs:
            try:
                image = Image.open(f"uploaded_files/{image}")

                response = self.gemini.client.models.generate_content(
                    model=model,
                    contents=[system_prompt, user_prompt, image],
                )
                raw_text = self.safe_extract_text(response)
                clean_text = raw_text.strip("```").replace("json", "").strip()

                try:
                    response = json.loads(clean_text)
                    self.data.append(response[0])

                    print(f'data 1: {self.data}')
                except json.JSONDecodeError:
                    print("⚠️ No se pudo parsear el JSON, texto crudo:")

            except Exception as e:
                    raise Exception(f"Unexpected error: {str(e)}")

            return self.data

    @staticmethod
    def safe_extract_text(response):
        """Extrae texto de forma segura desde la respuesta Gemini."""
        if not response:
            return None
        try:
            parts = (
                response.candidates[0]
                .content.parts
            )
            if not parts:
                return None
            return getattr(parts[0], "text", None)
        except Exception:
            return None


