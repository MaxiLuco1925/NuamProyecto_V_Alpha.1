from django.test import Client
from django.urls import reverse
from usuarios.models import Usuario, Rol
from auditoria.models import CalificacionTributaria
from instrumentos.models import Mercado, Instrumento
import pytest
from declaraciones.models import CargaArchivo
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
import random   
from unittest import mock 
from django.contrib.auth.hashers import make_password

##################################################################################################
##----Pruebas de integracion--------------------------------------------------########################
###################################################################################################

# --- TestAuthFlowIntegration ---

@pytest.mark.integration # Marca la clase como prueba de integración
@pytest.mark.django_db # Asegura el acceso a la base de datos de Django para esta clase
class TestAuthFlowIntegration:    
    def setup_method(self):
        # 1. Configurar cliente HTTP de prueba
        self.client = Client()
        # 2. Obtener o crear el Rol necesario para el usuario de prueba
        # Asume que Rol.objects.get_or_create existe
        self.rol_corredor, _ = Rol.objects.get_or_create(descripcion="Corredor")
        
        # 3. Generar documento de identidad único para evitar colisiones en la DB
        doc_unique = f"{random.randint(10000000, 99999999)}"
        
        # 4. Obtener o crear un usuario de prueba para la autenticación
        # Asume que Usuario.objects.get_or_create existe
        self.usuario, _ = Usuario.objects.get_or_create(
            documento_identidad=doc_unique,
            defaults={
                'nombre': "Test User",
                'email': f"test{doc_unique}@example.com",
                'contraseña_hash': "1234", 
                'verificado': True,
                'rol': self.rol_corredor
            }
        )
    
    # -------------------------------------------------------------------
    
    def test_flujo_completo_login_panel(self):        
        # 1. Iniciar sesión estableciendo manualmente la sesión del cliente
        session = self.client.session # Obtiene la sesión actual del cliente
        session["usuario_id"] = self.usuario.id # Simula la autenticación guardando el ID de usuario
        session.save() # Guarda los cambios en la sesión
        
        # 2. Acceder al panel principal (ruta protegida)
        panel_url = reverse("interfazinicio") # Resuelve la URL por su nombre ('interfazinicio')
        response = self.client.get(panel_url) # Realiza una petición GET a la URL
        
        # 3. Verificar integración exitosa (acceso concedido)
        assert response.status_code == 200 # Espera un código de estado 200 (OK)
        assert "Usuario" in response.context # Verifica que el contexto contenga la clave "Usuario"
        assert response.context["Usuario"] == self.usuario # Verifica que el usuario en el contexto sea el correcto
        
        # 4. Verificar que la sesión persiste
        assert self.client.session["usuario_id"] == self.usuario.id # Revisa que el ID de usuario siga en la sesión
    
    # -------------------------------------------------------------------
    
    def test_flujo_redireccion_protegida(self):
        # 1. Intentar acceder a panel sin haber configurado sesión
        panel_url = reverse("interfazinicio") # Resuelve la URL del panel principal
        response = self.client.get(panel_url) # Realiza una petición GET sin sesión
        
        # 2. Verificar redirección
        assert response.status_code == 302 # Espera un código 302 (Redirección)
        assert "iniciarSesion" in response.url # Verifica que la redirección apunte a la página de login
    
    # -------------------------------------------------------------------

    def test_acceso_rol_protegido_integracion(self):        
        # 1. Configurar sesión para el usuario (que tiene el rol "Corredor")
        session = self.client.session
        session["usuario_id"] = self.usuario.id
        session.save()
        
        # 2. Acceder a vista que requiere rol específico
        carga_url = reverse("carga_montos") # Resuelve la URL de la vista protegida por rol
        response = self.client.get(carga_url) # Realiza la petición GET
        
        # 3. Verificar acceso concedido
        assert response.status_code == 200 # Espera 200, indicando que el rol es suficiente para el acceso
        assert "form" in response.context # Verifica la presencia de datos esperados en el contexto (e.g., el formulario)

# --- TestCargaMasivaIntegration ---

@pytest.mark.integration # Marca la clase como prueba de integración
@pytest.mark.django_db # Asegura el acceso a la base de datos de Django para esta clase
class TestCargaMasivaIntegration:
    """Pruebas de integración para flujo completo de carga masiva"""
    
    def setup_method(self):
        """Este método se ejecuta antes de CADA prueba"""
        
        # 1. Configurar cliente HTTP de prueba
        self.client = Client()
        
        # 2. Obtener o crear el Rol necesario
        self.rol_corredor, _ = Rol.objects.get_or_create(descripcion="Corredor")
        
        # 3. Generar documento único
        doc_unique = f"{random.randint(10000000, 99999999)}"
        
        # 4. Obtener o crear usuario
        self.usuario, _ = Usuario.objects.get_or_create(
            documento_identidad=doc_unique,
            defaults={
                'nombre': "Test User",
                'email': f"test{doc_unique}@example.com",
                'contraseña_hash': "1234",
                'verificado': True,
                'rol': self.rol_corredor
            }
        )
        
        # 5. Configurar sesión para autenticar al cliente de prueba
        session = self.client.session
        session["usuario_id"] = self.usuario.id
        session.save()
    
    # -------------------------------------------------------------------
    
    def test_flujo_completo_carga_masiva(self):
        """Integración: Autenticación → Formulario → Procesamiento → BD"""
        
        # 1. Acceder al formulario de carga (Paso GET)
        carga_url = reverse("carga_montos")
        response_get = self.client.get(carga_url)
        
        assert response_get.status_code == 200
        assert "form" in response_get.context
        
        # 2. Preparar archivo de prueba (simulando un archivo CSV)
        csv_content = "documento,monto,factor\n11111111,1000,1.5\n22222222,2000,2.0" # Contenido del CSV de prueba
        fake_file = SimpleUploadedFile(
            "test_integracion.csv",
            csv_content.encode('utf-8'), # Codifica el contenido a bytes
            content_type="text/csv"
        )
        
        # 3. Enviar formulario de carga (Paso POST)
        response_post = self.client.post(
            carga_url,
            {
                "archivo": fake_file, # El archivo simulado
                "tipo_carga": "montos:dj1948" # Otro campo del formulario
            },
            format="multipart" # Necesario para peticiones que contienen archivos
        )
        
        # 4. Verificar procesamiento completo (Redirección o renderización exitosa + BD)
        assert response_post.status_code == 200 # Espera éxito tras el POST (asume que no hay redirección)
        assert CargaArchivo.objects.count() == 1 # Verifica que se haya creado 1 registro en la base de datos
        
        carga = CargaArchivo.objects.first() # Recupera el objeto creado para inspeccionarlo
        assert carga.tipo_carga == "montos:dj1948" # Verifica que el tipo de carga sea el correcto
        assert carga.cargado_por == self.usuario # Verifica que la carga esté asociada al usuario autenticado
        assert "calificaciones" in response_post.context # Verifica el resultado del procesamiento en el contexto
    
    # -------------------------------------------------------------------
    
    def test_integracion_multiple_usuarios_carga(self):
        """Integración: Múltiples usuarios → Cargas separadas"""
        
        carga_url = reverse("carga_montos")
        
        # 1. Crear segundo usuario con documento único
        doc_unique2 = f"{random.randint(10000000, 99999999)}"
        usuario2, _ = Usuario.objects.get_or_create(
            documento_identidad=doc_unique2,
            defaults={
                'nombre': "User 2",
                'email': f"user2{doc_unique2}@example.com",
                'contraseña_hash': "1234",
                'verificado': True,
                'rol': self.rol_corredor
            }
        )
        
        # 2. Usuario 1 hace carga (sesión ya configurada en setup_method, pero se reconfirma)
        session = self.client.session
        session["usuario_id"] = self.usuario.id # Asegura que la sesión es del Usuario 1
        session.save()
        
        csv1 = SimpleUploadedFile("user1.csv", b"data1", content_type="text/csv")
        response1 = self.client.post(carga_url, {"archivo": csv1, "tipo_carga": "montos:dj1948"})
        assert response1.status_code == 200
        
        # 3. Usuario 2 hace carga (cambiando la sesión)
        session["usuario_id"] = usuario2.id # Cambia la sesión al Usuario 2
        session.save()
        
        csv2 = SimpleUploadedFile("user2.csv", b"data2", content_type="text/csv")
        response2 = self.client.post(carga_url, {"archivo": csv2, "tipo_carga": "montos:dj1948"})
        assert response2.status_code == 200
        
        # 4. Verificar que las cargas están separadas y asociadas al usuario correcto
        assert CargaArchivo.objects.count() == 2 # Espera 2 registros totales
        cargas_usuario1 = CargaArchivo.objects.filter(cargado_por=self.usuario) # Filtra por Usuario 1
        cargas_usuario2 = CargaArchivo.objects.filter(cargado_por=usuario2) # Filtra por Usuario 2
        
        assert cargas_usuario1.count() == 1 # Verifica 1 carga para el Usuario 1
        assert cargas_usuario2.count() == 1 # Verifica 1 carga para el Usuario 2
        
# 1. Verificar que pytest detecta los tests
# pytest Test/Test_usuarios/ --collect-only

# 2. Ejecutar todas las pruebas de integración
#pytest Test/Test_usuarios/ -v -m integration

##################################################################
#----Pruebas unitarias de vistas---------------------------------##
#################################################################################
@pytest.mark.django_db
def test_portada_view(client):
    url = reverse('portada')
    response = client.get(url)
    assert response.status_code == 200
    assert "index.html" in [t.name for t in response.templates]

@pytest.mark.django_db
@mock.patch("usuarios.views.send_mail")
def test_registro_view(mock_send_mail, client):
    url = reverse('registro')
    
    datos_registro_validos = {
        'documento_identidad': '20123456-7',
        'nombre': 'Prueba Test',
        'email': 'prueba.registro@example.com',
        'genero': 'HOMBRE',
        'telefono': '911112222',
        'edad': 25,
        'pais': 'Chile',
        'region': 'Biobío',
        'comuna': 'Concepción',
        'password1': 'Passwordsegura123@', 
        'password2': 'Passwordsegura123@', 
    }
    

    response = client.post(url, data=datos_registro_validos, follow=False)
    
    assert response.status_code == 302
    assert response.url == reverse('verificacion') 
    
    assert Usuario.objects.filter(email='prueba.registro@example.com').exists()
    
    mock_send_mail.assert_called_once()



CODIGO_PRUEBA = '123456'
@pytest.mark.django_db
class TestVerificarCodigo:
    @pytest.fixture
    def usuario_no_verificado(self):
        return Usuario.objects.create(
            documento_identidad='11223344-5',
            nombre='Codigo Test',
            email='codigo.test@example.com',
            contraseña_hash=make_password('testpass'),
            verificado=False 
        )
    def test_verificar_codigo_get_cargacorreto(self, client):
        url = reverse('verificacion')
        response = client.get(url)
        assert response.status_code == 200
        assert 'Verificacion.html' in [t.name for t in response.templates]
    
    def test_verificar_codigo_post_exitoso(self, client, usuario_no_verificado):
        url = reverse('verificacion')

        session = client.session
        session['codigo_verificacion'] = CODIGO_PRUEBA
        session['usuario_id'] = usuario_no_verificado.id
        session.save() 
        response = client.post(url, data={'codigo': CODIGO_PRUEBA}, follow=False)

        
        assert response.status_code == 302
        assert response.url == reverse('iniciarSesion')

        usuario_actualizado = Usuario.objects.get(id=usuario_no_verificado.id)
        assert usuario_actualizado.verificado is True

        session_after = client.session 
        assert 'codigo_verificacion' not in session_after

    def test_verificar_codigo_post_incorrecto(self, client, usuario_no_verificado):
    
        url = reverse('verificacion')
        
        session = client.session
        session['codigo_verificacion'] = CODIGO_PRUEBA
        session['usuario_id'] = usuario_no_verificado.id
        session.save()

        response = client.post(url, data={'codigo': '999999'}, follow=False)


        assert response.status_code == 200
        assert 'Verificacion.html' in [t.name for t in response.templates]

        usuario_sin_cambios = Usuario.objects.get(id=usuario_no_verificado.id)
        assert usuario_sin_cambios.verificado is False




@pytest.mark.django_db
class TestIniciarSesion:
    @pytest.fixture
    def usuario_base(self):
        """Fixture base para crear un usuario verificado y listo para login."""
        return Usuario.objects.create(
            documento_identidad='10111222-3',
            nombre='Login Test',
            email='login.test@example.com',
            contraseña_hash=make_password('Password123'), # Contraseña conocida
            verificado=True
        )

    @pytest.fixture
    def usuario_no_verificado(self):
        """Fixture para un usuario que NO ha completado la verificación."""
        return Usuario.objects.create(
            documento_identidad='20333444-5',
            nombre='Unverified Test',
            email='unverified.test@example.com',
            contraseña_hash=make_password('Password123'),
            verificado=False
        )

    # Datos que el formulario POST debe enviar
    DATOS_LOGIN_VALIDOS = {
        'documento_identidad': '10111222-3',
        'contraseña': 'Password123',
    }
    
    # ----------------------------------------------------------------------
    # --- ESCENARIO 1: GET (Carga de página) ---
    
    def test_iniciar_sesion_get_carga_correcto(self, client):
        """Verifica que la página de login cargue con 200."""
        url = reverse('iniciarSesion')
        response = client.get(url)
        assert response.status_code == 200
        assert 'InicioSesion.html' in [t.name for t in response.templates]

    # ----------------------------------------------------------------------
    # --- ESCENARIO 2: POST EXITOSO (Documento y Contraseña Correctos) ---

    def test_iniciar_sesion_post_exitoso(self, client, usuario_base):
        """Verifica que un usuario verificado inicie sesión y sea redirigido."""
        url = reverse('iniciarSesion')
        
        # Datos de login del usuario_base
        datos = self.DATOS_LOGIN_VALIDOS.copy()
        
        response = client.post(url, data=datos, follow=False)

        # 1. Aserción de redirección a la interfaz
        assert response.status_code == 302
        assert response.url == reverse('interfazinicio')
        
        # 2. Aserción de sesión: Verifica que la sesión se inicializó
        assert client.session.get('usuario_id') == usuario_base.id
        assert client.session.get('usuario_nombre') == usuario_base.nombre


    # ----------------------------------------------------------------------
    # --- ESCENARIO 3: POST FALLIDO (Contraseña Incorrecta) ---

    def test_iniciar_sesion_contraseña_incorrecta(self, client, usuario_base):
        """Verifica que con contraseña incorrecta no haya login y se quede en la página."""
        url = reverse('iniciarSesion')
        
        datos = self.DATOS_LOGIN_VALIDOS.copy()
        datos['contraseña'] = 'ContraseñaFalsa' # Contraseña incorrecta
        
        response = client.post(url, data=datos, follow=False)

        # 1. Aserción de respuesta: Se queda en la misma página (200)
        assert response.status_code == 200
        assert 'InicioSesion.html' in [t.name for t in response.templates]
        
        # 2. Aserción de sesión: No debe haber login
        assert 'usuario_id' not in client.session


    # ----------------------------------------------------------------------
    # --- ESCENARIO 4: POST FALLIDO (Documento Inexistente) ---

    def test_iniciar_sesion_documento_inexistente(self, client):
        """Verifica que si el documento no existe, se quede en la página y muestre el mensaje correcto."""
        url = reverse('iniciarSesion')

        datos = self.DATOS_LOGIN_VALIDOS.copy()
        datos['documento_identidad'] = '99999999-9' # Documento que no existe
        datos['contraseña'] = 'Password123'

        response = client.post(url, data=datos, follow=False)

        # 1. Aserción de respuesta: Se queda en la misma página (200)
        assert response.status_code == 200

        # 2. Aserción de mensaje: Verifica que el mensaje de error sea EXACTO
        messages_list = [str(m.message) for m in response.context['messages']]
        
        # Corregido: Verificar el mensaje sin el emoji
        assert "Credenciales inválidas." in messages_list[0]

    # ----------------------------------------------------------------------
    # --- ESCENARIO 5: POST FALLIDO (Usuario No Verificado) ---

    def test_iniciar_sesion_no_verificado_redirige(self, client, usuario_no_verificado):
        """Verifica que si el usuario no está verificado, sea redirigido a 'verificacion'."""
        url = reverse('iniciarSesion')
        
        # Datos de login del usuario_no_verificado
        datos = {
            'documento_identidad': usuario_no_verificado.documento_identidad,
            'contraseña': 'Password123',
        }
        
        response = client.post(url, data=datos, follow=False)

        # 1. Aserción de redirección a verificación
        assert response.status_code == 302
        assert response.url == reverse('verificacion')
        
        # 2. Aserción de sesión: No debe haber login completo
        assert 'usuario_id' not in client.session
