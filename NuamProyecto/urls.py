"""
URL configuration for NuamProyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from usuarios.views import portada, iniciarSesion, registro, interfazinicio, market_data_api, Administrador, panel, panelAdmin, EditarRolusuario, adminEliminarUsuario, listausuarios
from auditoria.views import cargaArchivos,x_factor, Configuración, ConfiguraciónAdmin, verificacionUsuario, reportes, Factor, x_monto, x_factor_Admin, x_monto_Admin,lecturaReportes,listadoUsuario
from declaraciones.views  import ingresarCalificacion

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', portada, name='portada'),
    path('iniciarSesion/', iniciarSesion, name='iniciarSesion'),
    path('registro/', registro, name = 'registro' ),
    path('interfazinicio/', interfazinicio,name='interfazinicio'),
    path('api/acciones_data/', market_data_api, name='acciones_data'),
    path('interfazAdmin/', Administrador,name="interfazAdmin"),
    path('configuracion/', Configuración, name='Configuración'),
    path('configuracionAdmin/', ConfiguraciónAdmin, name='ConfiguraciónAdmin'),
    path('Verificacion/',verificacionUsuario,name='Verificacion'),
    path('Reportes/',reportes,name="Reportes"),
    path('panelCalificacion/', panel, name='panelCalificacion' ),
    path('panelCalificacionAdmin/', panelAdmin, name='panelCalificacionAdmin'),
    path('FactorImp/',Factor,name='FactorImp'),
    path('x_factor/', x_factor, name='x_factor'),
    path('x_factor_Admin/', x_factor_Admin, name='x_factor_Admin'),
    path('x_monto/', x_monto, name='x_monto'),
    path('x_monto_Admin/', x_monto_Admin, name='x_monto_Admin'),
    path('listadoUsuario/', listadoUsuario, name='listadoUsuario'),
    path('listausuarios/<int:pk>/editar/', EditarRolusuario, name='EditarRolusuario'),
    path('listausuarios/<int:pk>/eliminar/', adminEliminarUsuario, name='adminEliminarUsuario'),
    path('listausuarios/', listausuarios, name='listausuarios'),
    path('lecturaReportes/', lecturaReportes, name='lecturaReportes'),
    path('cargaArchivos', cargaArchivos, name='cargaArchivos'),
    path('ingresarCalificacion/', ingresarCalificacion, name='ingresarCalificacion'),

]

