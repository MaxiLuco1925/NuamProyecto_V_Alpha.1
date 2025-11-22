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
from django.urls import path
from usuarios.views import portada, iniciarSesion, registro, interfazinicio, market_data_api, Administrador, panel, panelAdmin, EditarRolusuario, adminEliminarUsuario, listausuarios,salir, descargar_calificacion,ver_detalle_calificacion,editar_calificacion_manual,eliminar_calificacion, verificar_codigo, auditoriaSesiones,panelArchivoXFactor, panelArchivoXFactorAdmin, descargar_calificacion_Admin, ver_detalle_calificacion_Admin, editar_calificacion_manual_Admin
from auditoria.views import cargaArchivos, Configuración, ConfiguraciónAdmin, verificacionUsuario, reportes, Factor,lecturaReportes,listadoUsuario, FactorAdmin
from declaraciones.views  import ingresarCalificacion, x_factorCalculo, ingresarCalificacionAdmin, x_factorCalculoAdmin,ProcesarArchivoCSV, carga_masiva_factores_view, carga_masiva_montos_view, ProcesarArchivoMontosCSV, carga_masiva_montos_Admin, carga_masiva_factores_Admin

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
    path('auditoria/sesiones/',auditoriaSesiones, name="auditoriaSesiones" ),
    path('FactorImp/',Factor,name='FactorImp'),
    path('FactorAdminList/',FactorAdmin,name='FactorAdminList'),
    path('carga/factores/', carga_masiva_factores_view, name='carga_factores'),
    path('carga/montos/', carga_masiva_montos_view, name='carga_montos'),
    path('listadoUsuario/', listadoUsuario, name='listadoUsuario'),
    path('listausuarios/<int:pk>/editar/', EditarRolusuario, name='EditarRolusuario'),
    path('listausuarios/<int:pk>/eliminar/', adminEliminarUsuario, name='adminEliminarUsuario'),
    path('listausuarios/', listausuarios, name='listausuarios'),
    path('lecturaReportes/', lecturaReportes, name='lecturaReportes'),
    path('cargaArchivos', cargaArchivos, name='cargaArchivos'),
    path('ingresarCalificacion/', ingresarCalificacion, name='ingresarCalificacion'),
    path("factor_listado/", x_factorCalculo, name = "factorListado" ),
    path('salir/', salir, name= 'salir'),
    path('descargar/<int:calificacion_id>/', descargar_calificacion, name='descargar_calificacion'),
    path('descargar_Admin/<int:calificacion_id>/', descargar_calificacion_Admin, name='descargar_calificacion_Admin'),
    path('calificacion/<int:calificacion_id>/detalle/', ver_detalle_calificacion, name='ver_detalle_calificacion'),
    path('calificacion_Admin/<int:calificacion_id>/detalle/', ver_detalle_calificacion_Admin, name='ver_detalle_calificacion_Admin'),
    path('ingresarcalificacionAdmin/', ingresarCalificacionAdmin, name= "calificacionAdmin"),
    path("factorAdmin/", x_factorCalculoAdmin, name = "factorAdmin"),
    path('editar/<int:pk>/', editar_calificacion_manual, name='editar_calificacion'),
    path('editar_Admin/<int:pk>/', editar_calificacion_manual_Admin, name='editar_calificacion_Admin'),
    path('eliminar/<int:pk>/', eliminar_calificacion, name='eliminar_calificacion'),
    path('verificacion/', verificar_codigo, name='verificacion'),
    path('ProcesarArchivoCSV/', ProcesarArchivoCSV, name='ProcesarArchivoCSV'),
    path('ProcesarArchivoMontosCSV/', ProcesarArchivoMontosCSV, name = 'ProcesarArchivoMontosCSV'),
    path('panel/archivo-x-factor/', panelArchivoXFactor, name='panelArchivoXFactor'),
    path('carga/montos_Admin/', carga_masiva_montos_Admin, name='carga_montos_Admin'),
    path('carga/factores_Admin/', carga_masiva_factores_Admin, name='carga_factores_Admin'),
    path('panel/archivo-x-factor_admin/', panelArchivoXFactorAdmin,  name='panelArchivoXFactorAdmin'),

]

