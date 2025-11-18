from .google_clients.gemini_client import GeminiClient
from typing import List
import json
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

class Gemini:
    def __init__(self, imgs:List[str]):
        self.imgs=imgs
        self.data: list[dict] = []
        self.gemini = GeminiClient()
        self.model = "gemini-2.0-flash"
        self.system_prompt = """
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
            - El campo "total" debe estar en formato estándar con coma decimal. p.ej "1234.56" debe ser "1234,56".
            - Usa sentido común y el nombre del proveedor o productos para inferir la categoría.
            - Estandariza los valores numéricos a dos decimales (con punto decimal).
            - Si hay varias facturas, devuelve una lista JSON con cada una como objeto independiente.
            """
        self.user_prompt = """
            Analiza las siguientes imágenes de facturas y devuelve, en formato JSON, los campos:
            num_de_documento, fecha, proveedor,NIF_CIF, tipo_material, total.
            """

    def process_image(self, image_name: str):
        """Procesa una imagen individualmente con Gemini."""
        try:
            image_path = f"uploaded_files/{image_name}"
            image = Image.open(image_path)

            response = self.gemini.client.models.generate_content(
                model=self.model,
                contents=[self.system_prompt, self.user_prompt, image],
            )

            raw_text = self.safe_extract_text(response)
            if not raw_text:
                print(f"⚠️ Sin respuesta válida para {image_name}")
                return None

            clean_text = raw_text.strip("```").replace("json", "").strip()

            try:
                json_response = json.loads(clean_text)
                if isinstance(json_response, list):
                    return json_response[0]
                elif isinstance(json_response, dict):
                    return json_response
                else:
                    print(f"⚠️ Formato JSON inesperado para {image_name}")
                    return None
            except json.JSONDecodeError:
                print(f"⚠️ Error parseando JSON en {image_name}")
                return None

        except Exception as e:
            print(f"❌ Error procesando {image_name}: {e}")
            return None

    def get_result(self):

        """Procesa todas las imágenes en paralelo y guarda los resultados en self.data."""
        results = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(self.process_image, img): img for img in self.imgs}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
                    print(f"✅ Procesada: {futures[future]}")
                else:
                    print(f"⚠️ Sin datos para {futures[future]}")
        self.data = results
        print(f"📦 Total facturas procesadas: {len(self.data)}")
        return self.data

    @staticmethod
    def safe_extract_text(response):
        """Extrae texto de forma segura desde la respuesta Gemini."""
        if not response:
            return None
        try:
            parts = response.candidates[0].content.parts
            if not parts:
                return None
            return getattr(parts[0], "text", None)
        except Exception:
            return None


