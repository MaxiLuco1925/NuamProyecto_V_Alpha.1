import base64
import io
import numpy as np
from PIL import Image
import face_recognition

# Umbral de distancia. Menor = más estricto. 0.6 es el estándar recomendado
# por face_recognition para un balance entre falsos positivos y falsos negativos.
TOLERANCIA = 0.5


class RostroNoDetectadoError(Exception):
    pass


def _decodificar_imagen_base64(imagen_base64: str) -> np.ndarray:
    if "," in imagen_base64:
        imagen_base64 = imagen_base64.split(",", 1)[1]

    datos = base64.b64decode(imagen_base64)
    imagen = Image.open(io.BytesIO(datos)).convert("RGB")
    return np.array(imagen)


def generar_embedding(imagen_base64: str) -> np.ndarray:

    arreglo = _decodificar_imagen_base64(imagen_base64)

    ubicaciones = face_recognition.face_locations(arreglo, model="hog")
    if len(ubicaciones) == 0:
        raise RostroNoDetectadoError("No se detectó ningún rostro. Acércate más a la cámara y asegura buena luz.")
    if len(ubicaciones) > 1:
        raise RostroNoDetectadoError("Se detectó más de un rostro. Asegúrate de estar solo frente a la cámara.")

    embeddings = face_recognition.face_encodings(arreglo, known_face_locations=ubicaciones)
    return embeddings[0]


def comparar_embeddings(embedding_guardado: np.ndarray, embedding_actual: np.ndarray) -> tuple[bool, float]:
    distancia = np.linalg.norm(embedding_guardado - embedding_actual)
    return distancia <= TOLERANCIA, float(distancia)
