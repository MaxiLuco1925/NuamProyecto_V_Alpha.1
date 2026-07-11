import boto3
import json
from datetime import datetime
from django.conf import settings


class DynamoDBService:
    def __init__(self):
        # Si las variables AWS no existen, boto3 usa el perfil configurado con
        # ``aws configure``. Esto evita enviar credenciales vacías al cliente.
        parametros = {'region_name': settings.AWS_S3_REGION_NAME}
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            parametros.update({
                'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
                'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
            })
            if getattr(settings, 'AWS_SESSION_TOKEN', ''):
                parametros['aws_session_token'] = settings.AWS_SESSION_TOKEN

        self.dynamodb = boto3.resource('dynamodb', **parametros)
        
        # Tabla de Sesiones (ya existente)
        self.table_sesiones = self.dynamodb.Table(settings.DYNAMODB_SESSIONS_TABLE)
        
        # Tabla de Auditoría (la que creamos)
        self.table_auditoria = self.dynamodb.Table(settings.DYNAMODB_AUDIT_TABLE)

    def crear_sesion(self, usuario_id, documento, ip_origen, user_agent='N/A'):
        """Guarda la sesión en NUAM-Sessions"""
        try:
            ahora = datetime.now()
            session_id = f"{documento}_{ahora.strftime('%Y%m%d%H%M%S%f')}"
            
            self.table_sesiones.put_item(Item={
                'session_id': session_id,
                'usuario_id': str(usuario_id),
                'documento': documento,
                'ip_origen': ip_origen,
                'user_agent': user_agent,
                'estado': 'ACTIVA',
                'fecha_creacion': ahora.isoformat(),
                'timestamp': int(ahora.timestamp())
            })
            return {'exito': True, 'session_id': session_id}
        except Exception as e:
            print(f"Error sesión: {e}")
            return {'exito': False, 'error': str(e)}

    def registrar_auditoria(self, documento, tipo_evento, resultado, ip_origen='N/A', detalles=None):
        """Guarda el log en nuam_auditoria_seguridad"""
        try:
            ahora = datetime.now()
            evento_id = f"{documento}_{ahora.strftime('%Y%m%d%H%M%S%f')}"
            
            self.table_auditoria.put_item(Item={
                'evento_id': evento_id,
                'documento': documento,
                'tipo_evento': tipo_evento,
                'resultado': resultado,
                'ip_origen': ip_origen,
                'fecha_hora': ahora.isoformat(),
                'timestamp': int(ahora.timestamp()),
                'detalles': json.dumps(detalles or {})
            })
            return {'exito': True, 'evento_id': evento_id}
        except Exception as e:
            print(f"Error auditoría: {e}")
            return {'exito': False, 'error': str(e)}

    def obtener_sesiones_usuario(self, documento, limite=10):
        """Obtiene sesiones de un usuario"""
        try:
            response = self.table_sesiones.scan(
                FilterExpression='documento = :doc',
                ExpressionAttributeValues={':doc': documento},
                Limit=limite
            )
            return response.get('Items', [])
        except Exception as e:
            print(f"Error obteniendo sesiones: {e}")
            return []

    def obtener_ultimos_eventos_auditoria(self, limite=50):
        """Obtiene los últimos eventos de auditoría"""
        try:
            response = self.table_auditoria.scan(Limit=limite)
            items = response.get('Items', [])
            return sorted(items, key=lambda x: x.get('timestamp', 0), reverse=True)
        except Exception as e:
            print(f"Error obteniendo auditoría: {e}")
            return []
