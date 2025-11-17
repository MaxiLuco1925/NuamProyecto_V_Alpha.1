import pytest
from unittest import mock 
from usuarios.models import Usuario
from django.urls import reverse
from django.contrib.auth.hashers import make_password

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

    def test_iniciar_sesion_documento_inexistente(self,client):
        """Verifica que si el documento no existe, se quede en la página y muestre el mensaje correcto."""
        url = reverse('iniciarSesion')

        datos = self.DATOS_LOGIN_VALIDOS.copy()
        datos['documento_identidad'] = '99999999-9' # Documento que no existe
        
        # La contraseña también es necesaria, aunque el documento sea el que falle
        datos['contraseña'] = 'Password123' 

        response = client.post(url, data=datos, follow=False)

        # 1. Aserción de respuesta: Se queda en la misma página (200)
        assert response.status_code == 200

        # 2. Aserción de mensaje: Verifica que el mensaje de error sea EXACTO
        messages_list = [m.message for m in response.context['messages']]
        # Línea Corregida: Incluye el emoji '❌' para hacer coincidir el mensaje de la vista
        assert "❌ Credenciales inválidas." in messages_list
        
        # 3. Aserción de sesión: No debe haber login
        assert 'usuario_id' not in client.session

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