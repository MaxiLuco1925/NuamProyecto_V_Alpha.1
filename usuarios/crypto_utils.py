"""
Utilidades de cifrado para datos biométricos (embeddings faciales).

El embedding facial (vector numérico) NUNCA se guarda en texto plano.
Se cifra con Fernet (AES-128 en modo CBC + HMAC) usando una clave
simétrica que vive fuera del repositorio, en una variable de entorno.
"""
import os
import base64
import numpy as np
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings


def _get_fernet():
    key = getattr(settings, "FACE_ENCRYPTION_KEY", None) or os.environ.get("FACE_ENCRYPTION_KEY")
    if not key:
        raise RuntimeError(
            "FACE_ENCRYPTION_KEY no está configurada. Define esta variable de entorno "
            "antes de usar el reconocimiento facial (ver instrucciones de despliegue)."
        )
    return Fernet(key.encode() if isinstance(key, str) else key)


def encriptar_embedding(embedding: np.ndarray) -> bytes:
    """Convierte un embedding (np.ndarray float) en bytes cifrados listos para guardar en BD."""
    f = _get_fernet()
    raw_bytes = embedding.astype(np.float64).tobytes()
    return f.encrypt(raw_bytes)


def desencriptar_embedding(token: bytes) -> np.ndarray:
    """Revierte encriptar_embedding. Lanza InvalidToken si la clave no coincide o el dato fue alterado."""
    f = _get_fernet()
    try:
        raw_bytes = f.decrypt(bytes(token))
    except InvalidToken:
        raise ValueError("No se pudo desencriptar el perfil facial: token inválido o clave incorrecta.")
    return np.frombuffer(raw_bytes, dtype=np.float64)
