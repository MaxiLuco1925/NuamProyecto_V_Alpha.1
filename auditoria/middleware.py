
from usuarios.models import AuditoriaSesion, Usuario
from django.http import HttpResponseForbidden
import re

class SeguridadMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.patrones_ataque = {
            'SQL_INYECTION': [
                r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
                r"((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(\%3B)|(;))",
                r"union.*select",
                r"insert.*into",
                r"drop.*table",
                r"delete.*from",
                r"update.*set",
                r"exec(\s|\+)+(s|x)p\w+",
            ],
            'XSS': [
                r"<script.*?>.*?</script>",
                r"<img.*?onerror=.*?>",
                r"<iframe.*?src=.*?>",
                r"javascript:.*",
                r"onload=.*",
                r"onerror=.*",
                r"onclick=.*",
                r"alert\(.*\)",
            ],
            'CSRF': [
                r"csrfmiddlewaretoken.*=.*''",
                r"csrfmiddlewaretoken.*=.*null",
                r"csrfmiddlewaretoken.*=.*undefined",
            ]
        }

    def __call__(self, request):
        amenazas = self._analizar_request(request)
        
        if amenazas:
            self._registrar_amenazas(request, amenazas)
            
            if any(amenaza['nivel_amenaza'] in ['ALTO', 'CRITICO'] for amenaza in amenazas):
                return HttpResponseForbidden("Acceso bloqueado por seguridad")
        
        response = self.get_response(request)
        return response

    def _registrar_amenazas(self, request, amenazas):
        """Registrar amenazas directamente en AuditoriaSesion"""
        try:
            usuario = None
            documento_intentado = 'Anónimo'
            rol = 'N/A'
    
            if hasattr(request, 'user') and request.user.is_authenticated:
                try:
             
                    usuario = Usuario.objects.filter(id=request.user.id).first()
                    if usuario:
                        documento_intentado = usuario.documento_identidad
                        rol = usuario.rol.descripcion if usuario.rol else 'Sin rol'
                except Exception:
                    pass

       
            primera_amenaza = amenazas[0]
            
         
            tipos_ataque = set(amenaza['tipo_ataque'] for amenaza in amenazas)
            if 'SQL_INYECTION' in tipos_ataque:
                tipo_evento = 'INYECCION_SQL'
            elif 'XSS' in tipos_ataque:
                tipo_evento = 'XSS'
            elif 'CSRF' in tipos_ataque:
                tipo_evento = 'CSRF'
            else:
                tipo_evento = 'ACCESO_DENEGADO'
            
          
            niveles = [amenaza['nivel_amenaza'] for amenaza in amenazas]
            nivel_maximo = 'ALTO' if 'ALTO' in niveles else 'MEDIO'
            
            AuditoriaSesion.objects.create(
                usuario=usuario,
                documento_intentado=documento_intentado,
                exito=False,
                rol=rol,
                tipo_evento=tipo_evento,
                nivel_amenaza=nivel_maximo,
                ip_address=self._obtener_ip_cliente(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                detalles=f"Se detectaron {len(amenazas)} amenaza(s). Tipos: {', '.join(tipos_ataque)}",
                ruta_accedida=request.path,
                metodo_http=request.method,
                payload_intentado=primera_amenaza['payload'][:1000],  
                parametro_afectado=primera_amenaza['parametro'],
                tipo_ataque=primera_amenaza['tipo_ataque']
            )

        except Exception as e:
            print(f"Error registrando amenaza: {e}")

    def _analizar_request(self, request):
        """Analizar la request en busca de patrones maliciosos"""
        amenazas = []
    
        for param, value in request.GET.items():
            amenazas.extend(self._buscar_patrones(param, value, 'GET'))
        
  
        if request.method == 'POST':
            for param, value in request.POST.items():
                amenazas.extend(self._buscar_patrones(param, value, 'POST'))
        

        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if self._es_user_agent_malicioso(user_agent):
            amenazas.append({
                'tipo_ataque': 'XSS',
                'parametro': 'User-Agent',
                'payload': user_agent[:500],
                'metodo': 'HEADER',
                'nivel_amenaza': 'MEDIO'
            })
        
        return amenazas

    def _buscar_patrones(self, parametro, valor, metodo):
        """Buscar patrones de ataque en un valor específico"""
        detecciones = []
        valor_str = str(valor)
        
        for tipo_ataque, patrones in self.patrones_ataque.items():
            for patron in patrones:
                if re.search(patron, valor_str, re.IGNORECASE):
    
                    if tipo_ataque == 'SQL_INYECTION':
            
                        nivel_amenaza = 'ALTO'
                    elif tipo_ataque == 'XSS':
                        nivel_amenaza = 'MEDIO'
                    else:
                        nivel_amenaza = 'MEDIO'
                    
                    detecciones.append({
                        'tipo_ataque': tipo_ataque,
                        'parametro': parametro,
                        'payload': valor_str,
                        'metodo': metodo,
                        'nivel_amenaza': nivel_amenaza
                    })
                    break  
        
        return detecciones

    def _es_user_agent_malicioso(self, user_agent):
        """Detectar user agents que contengan payloads maliciosos"""
        patrones_maliciosos = [
            r"<script", r"javascript:", r"onload", r"onerror", r"alert\("
        ]
        return any(re.search(patron, user_agent, re.IGNORECASE) for patron in patrones_maliciosos)

    def _obtener_ip_cliente(self, request):
        """Obtener la IP real del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip