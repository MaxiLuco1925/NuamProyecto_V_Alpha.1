"""Persistencia de sesiones y eventos de seguridad en Azure Cosmos DB (NoSQL)."""

import logging
from datetime import datetime, timezone
from uuid import uuid4

from azure.cosmos import CosmosClient, PartitionKey
from django.conf import settings


logger = logging.getLogger(__name__)


class CosmosDBService:
    """Cliente perezoso para no impedir el arranque cuando Cosmos no está configurado."""

    def __init__(self):
        self._database = None
        self._sesiones = None
        self._auditoria = None

    def _conectar(self):
        if not getattr(settings, "COSMOS_DB_ENABLED", False):
            raise RuntimeError("Cosmos DB no está habilitado. Configure COSMOS_DB_ENABLED=True.")

        if self._database is not None:
            return

        connection_string = getattr(settings, "COSMOS_DB_CONNECTION_STRING", "")
        endpoint = getattr(settings, "COSMOS_DB_ENDPOINT", "")
        key = getattr(settings, "COSMOS_DB_KEY", "")

        if connection_string:
            client = CosmosClient.from_connection_string(connection_string)
        elif endpoint and key:
            client = CosmosClient(endpoint, credential=key)
        else:
            raise RuntimeError("Faltan las credenciales de Azure Cosmos DB.")

        database_name = settings.COSMOS_DB_DATABASE
        if getattr(settings, "COSMOS_AUTO_CREATE_CONTAINERS", False):
            self._database = client.create_database_if_not_exists(id=database_name)
            self._sesiones = self._database.create_container_if_not_exists(
                id=settings.COSMOS_SESSIONS_CONTAINER,
                partition_key=PartitionKey(path="/documento"),
            )
            self._auditoria = self._database.create_container_if_not_exists(
                id=settings.COSMOS_AUDIT_CONTAINER,
                partition_key=PartitionKey(path="/documento"),
            )
        else:
            self._database = client.get_database_client(database_name)
            self._sesiones = self._database.get_container_client(settings.COSMOS_SESSIONS_CONTAINER)
            self._auditoria = self._database.get_container_client(settings.COSMOS_AUDIT_CONTAINER)

    @staticmethod
    def _ahora():
        return datetime.now(timezone.utc)

    def crear_sesion(self, usuario_id, documento, ip_origen, user_agent="N/A", session_key=""):
        """Registra una sesión iniciada, con el mismo propósito que NUAM-Sessions en DynamoDB."""
        try:
            self._conectar()
            ahora = self._ahora()
            session_id = f"{documento}_{ahora.strftime('%Y%m%d%H%M%S%f')}_{uuid4().hex[:8]}"
            item = {
                "id": session_id,
                "session_id": session_id,
                "usuario_id": str(usuario_id),
                "documento": str(documento),
                "django_session_key": session_key,
                "ip_origen": ip_origen or "N/A",
                "user_agent": user_agent or "N/A",
                "estado": "ACTIVA",
                "fecha_creacion": ahora.isoformat(),
                "timestamp": int(ahora.timestamp()),
                "tipo": "sesion",
            }
            self._sesiones.upsert_item(item)
            return {"exito": True, "session_id": session_id}
        except Exception as error:
            logger.exception("No se pudo guardar la sesión en Cosmos DB")
            return {"exito": False, "error": str(error)}

    def registrar_auditoria(self, documento, tipo_evento, resultado, ip_origen="N/A", detalles=None):
        """Registra eventos de seguridad en el contenedor de auditoría de Cosmos DB."""
        try:
            self._conectar()
            ahora = self._ahora()
            evento_id = f"{documento}_{ahora.strftime('%Y%m%d%H%M%S%f')}_{uuid4().hex[:8]}"
            item = {
                "id": evento_id,
                "evento_id": evento_id,
                "documento": str(documento),
                "tipo_evento": tipo_evento,
                "resultado": resultado,
                "ip_origen": ip_origen or "N/A",
                "fecha_hora": ahora.isoformat(),
                "timestamp": int(ahora.timestamp()),
                "detalles": detalles or {},
                "tipo": "auditoria",
            }
            self._auditoria.upsert_item(item)
            return {"exito": True, "evento_id": evento_id}
        except Exception as error:
            logger.exception("No se pudo guardar la auditoría en Cosmos DB")
            return {"exito": False, "error": str(error)}

    def obtener_sesiones_usuario(self, documento, limite=10):
        try:
            self._conectar()
            limite = max(1, min(int(limite), 100))
            consulta = f"SELECT TOP {limite} * FROM c WHERE c.documento = @documento ORDER BY c.timestamp DESC"
            return list(self._sesiones.query_items(
                query=consulta,
                parameters=[{"name": "@documento", "value": str(documento)}],
                partition_key=str(documento),
            ))
        except Exception:
            logger.exception("No se pudieron obtener sesiones desde Cosmos DB")
            return []

    def obtener_ultimos_eventos_auditoria(self, limite=50):
        try:
            self._conectar()
            limite = max(1, min(int(limite), 100))
            consulta = f"SELECT TOP {limite} * FROM c ORDER BY c.timestamp DESC"
            return list(self._auditoria.query_items(
                query=consulta,
                enable_cross_partition_query=True,
            ))
        except Exception:
            logger.exception("No se pudieron obtener eventos desde Cosmos DB")
            return []
