from django.test import TestCase, Client
from django.urls import reverse
from .models import Usuario, Rol
from auditoria.models import CalificacionTributaria
from instrumentos.models import Mercado, Instrumento
from declaraciones.models import CargaArchivo
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from django.utils import timezone


# =========================================================
# CLASE 1 — Tests del Panel Principal
# =========================================================
# Asumimos que Usuario, Mercado, Instrumento, CalificacionTributaria 
# son modelos definidos en tu aplicación.

class PanelFunctionalTests(TestCase): # Define la clase de prueba funcional.

    def setUp(self): # Método que se ejecuta antes de cada prueba (test_...).
        self.client = Client() # Inicializa el cliente para simular las peticiones HTTP.

        # --- Preparación de datos de prueba ---
        # Crea un objeto Usuario en la base de datos de prueba.
        self.usuario = Usuario.objects.create(
            nombre="Test User",
            documento_identidad="11111111",
            email="test@example.com",
            contraseña_hash="1234",
            verificado=True,
        )

        # Crea un objeto Mercado.
        self.mercado = Mercado.objects.create(nombre="Bolsa X")
        
        # Crea un objeto Instrumento y lo relaciona con el Mercado.
        self.instrumento = Instrumento.objects.create(
            nombre="Instrumento Test", mercado=self.mercado
        )

        # Crea un objeto CalificacionTributaria con todos los campos necesarios, 
        # relacionándolo con el usuario y el instrumento creados.
        self.calificacion = CalificacionTributaria.objects.create(
            usuario=self.usuario,
            instrumento=self.instrumento,
            descripcion="Test Desc",
            fecha_pago=timezone.now(), # Usa la hora actual sensible a la zona horaria.
            secuencia_evento=1,
            dividendo=10.0,
            valor_historico=20.0,
            año_tributario=2025
        )

        # Obtiene la URL principal del panel de inicio usando su nombre ('interfazinicio').
        self.url = reverse("interfazinicio")

    def iniciar_sesion(self): # Función de utilidad para autenticar al usuario en el cliente.
        session = self.client.session # Obtiene la sesión actual del cliente.
        session["usuario_id"] = self.usuario.id # Asigna el ID del usuario a la sesión.
        session.save() # Guarda los cambios en la sesión.

    # --- Test 1: Acceso con Sesión (GET exitoso) ---
    def test_acceso_con_sesion(self): # Prueba el acceso exitoso a la interfaz de inicio.
        self.iniciar_sesion() # Autentica al usuario.
        response = self.client.get(self.url) # Simula una petición GET al panel.

        self.assertEqual(response.status_code, 200) # Verifica que el acceso sea exitoso (código 200 OK).
        # Verifica que se haya usado la plantilla esperada.
        self.assertTemplateUsed(response, "interfazinicio.html") 

        # Verifica que la vista haya pasado el objeto 'Usuario' al contexto de la plantilla.
        self.assertIn("Usuario", response.context)
        # Verifica que la vista haya pasado la cuenta total de calificaciones al contexto.
        self.assertIn("total_calificaciones", response.context)

    # --- Test 2: Redirección sin Sesión ---
    def test_redireccion_sin_sesion(self): # Prueba que la vista exige autenticación.
        # No se llama a self.iniciar_sesion(), por lo que el usuario no está autenticado.
        response = self.client.get(self.url) # Simula una petición GET.
        
        self.assertEqual(response.status_code, 302) # Verifica que haya una redirección (código 302).
        # Verifica que la URL de destino de la redirección contenga 'iniciarSesion'.
        self.assertIn("iniciarSesion", response.url) 

    # --- Test 3: Filtrado por Mercado (Funcionalidad Específica) ---
    def test_filtro_por_mercado(self): # Prueba que el filtrado por parámetro GET funciona.
        self.iniciar_sesion() # Autentica al usuario.
        
        # Simula una petición GET con el parámetro 'mercado' usando el ID creado.
        response = self.client.get(self.url, {"mercado": self.mercado.id}) 
        
        self.assertEqual(response.status_code, 200) # Verifica que la página cargue correctamente después del filtro.
        # Verifica que se use la plantilla correcta (la vista no debe cambiar de plantilla al filtrar).
        self.assertTemplateUsed(response, "interfazinicio.html") 
        
        # NOTA: Para hacer esta prueba más completa (funcional), deberías:
        # 1. Crear una segunda calificación de OTRO mercado.
        # 2. Verificar que 'response.context['calificaciones']' solo contenga 1 resultado (el filtrado).
        # Esto valida que el filtro realmente esté funcionando en la consulta a la BD.


# =========================================================
# CLASE 2 — Tests de Carga Masiva de Montos
# =========================================================
# Asumimos que Rol, Usuario, CargaArchivo están definidos en algún lugar (ej: .models)
# y que el decorador de rol está funcionando correctamente en la vista.

class CargaMasivaMontosTests(TestCase): # Define la clase de prueba que hereda de TestCase.

    def setUp(self): # Método que se ejecuta antes de cada prueba (test_...).
        self.client = Client() # Inicializa el cliente de pruebas para simular peticiones HTTP.

        # Crear rol requerido por el decorador
        # Crea un objeto Rol en la base de datos de prueba.
        self.rol_corredor = Rol.objects.create(descripcion="Corredor") 


        # Crea un objeto Usuario en la base de datos de prueba para la autenticación.
        self.usuario = Usuario.objects.create(
            nombre="Test User",
            documento_identidad="11111111",
            email="test@example.com",
            contraseña_hash="1234",
            verificado=True,
            rol=self.rol_corredor # Asigna el rol requerido.
        )


        # Configura la sesión del cliente con el ID del usuario creado.
        self.client.session["usuario_id"] = self.usuario.id
        # Guarda los cambios en la sesión para que estén disponibles en las peticiones.
        self.client.session.save() 

        # Obtiene la URL de la vista 'carga_montos' usando su nombre.
        self.url = reverse("carga_montos")

    def iniciar_sesion(self): # Función de utilidad para asegurar que el usuario está en la sesión.
        session = self.client.session # Obtiene la sesión actual del cliente.
        session["usuario_id"] = self.usuario.id # Establece la clave de usuario.
        session.save() # Guarda la sesión.

    # --- Prueba de Redirección ---
    def test_redireccion_sin_sesion(self): # Prueba que requiere que el usuario no esté autenticado.
        self.client.session.flush() # Elimina todos los datos de la sesión (desautentica al usuario).
        response = self.client.get(self.url) # Simula una petición GET a la URL de carga.
        self.assertEqual(response.status_code, 302) # Verifica que se produzca una redirección (código 302).
        self.assertIn("iniciarSesion", response.url) # Verifica que la URL de destino de la redirección contenga "iniciarSesion".

    # --- Prueba de Acceso (GET) ---
    def test_acceso_con_sesion(self): # Prueba que requiere que el usuario esté autenticado.
        self.iniciar_sesion() # Asegura que la sesión esté configurada para el usuario.
        response = self.client.get(self.url) # Simula una petición GET a la URL de carga.

        self.assertEqual(response.status_code, 200) # Verifica que el acceso sea exitoso (código 200).
        # Verifica que la plantilla específica para la carga de montos haya sido usada.
        self.assertTemplateUsed(response, "archivo_x_montos.html") 

        # Verifica que la vista pase el objeto formulario al contexto de la plantilla.
        self.assertIn("form", response.context)
        # Verifica que la vista pase los datos de rango de montos al contexto.
        self.assertIn("rango_montos", response.context)
        # Verifica que la vista pase los datos de rango de factores al contexto.
        self.assertIn("rango_factores", response.context)

    # --- Prueba de Subida (POST) ---
    # Reemplaza la clase de procesamiento real con un mock.
    @patch("declaraciones.views.ProcesarArchivoMontosCSV") 
    def test_subida_archivo_csv(self, mock_procesar): # El mock reemplaza el primer argumento.
        self.iniciar_sesion() # Asegura que la sesión esté configurada.

        # Configura el mock para que devuelva una lista de resultados simulados.
        mock_procesar.return_value = ["ok1", "ok2"]

        # Crea un archivo CSV simulado con contenido binario para la subida.
        fake_file = SimpleUploadedFile(
            "test.csv", b"campo1,campo2\n10,20", content_type="text/csv"
        )

        # Simula una petición POST de subida de archivo.
        response = self.client.post(
            self.url,
            {
                "archivo": fake_file, # Envía el archivo simulado.
                "tipo_carga": "montos:dj1948"  # Envía el tipo de carga requerido por el formulario.
            },
            format="multipart" # Indica que es una subida de archivo (multipart/form-data).
        )

        # Verifica que el código de estado de la respuesta HTTP sea 200 (OK).
        self.assertEqual(response.status_code, 200)
        # Verifica que se haya creado exactamente un registro en la BD para 'CargaArchivo'.
        self.assertEqual(CargaArchivo.objects.count(), 1) 

        # Recupera el objeto 'CargaArchivo' recién creado de la base de datos de prueba.
        carga = CargaArchivo.objects.first()
        
        # Verifica que el campo 'tipo_carga' del objeto guardado coincida con el valor enviado.
        self.assertEqual(carga.tipo_carga, "montos:dj1948") 
        
        # Verifica que el campo 'cargado_por' esté correctamente asociado al usuario autenticado.
        self.assertEqual(carga.cargado_por, self.usuario) 

        # Verifica que la función 'ProcesarArchivoMontosCSV' haya sido llamada exactamente una vez.
        mock_procesar.assert_called_once()
        
        # Verifica que la clave 'calificaciones' en el contexto contenga el valor de retorno simulado por el mock.
        self.assertEqual(response.context["calificaciones"], ["ok1", "ok2"])                