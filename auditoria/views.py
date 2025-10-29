from django.shortcuts import render
from usuarios.models import Usuario
from usuarios.models import Usuario

def x_factor(request):
    return render(request, 'archivo_x_factor.html')

def x_monto(request):
    return render(request, 'archivo_x_monto.html')

def x_factor_Admin(request):
    return render(request, 'archivo_x_factorAdmin.html')

def x_monto_Admin(request):
    return render(request, 'archivo_x_montoAdmin.html' )

def listadoUsuario(request):
    usuarios = Usuario.objects.all()
    data = {'usuarios' : usuarios}
    return render(request, 'listadoUsuario.html', data)

def lecturaReportes(request):
    return render(request, 'lecturaReportes.html')

def Factor(request):
    factores = range(8, 38)
    contexto = {'factores': factores}
    return render(request,'FactorImpuestos.html',contexto)

def Configuración(request):
    usuarios = Usuario.objects.all()
    data = {'usuarios' : usuarios}
    return render(request, 'configuracion.html', data)

def ConfiguraciónAdmin(request):
    return render(request, 'configuracionAdmin.html')

def verificacionUsuario(request):
    return render(request,"Verificacion.html")

def reportes(request):
    return render(request,'Reportes.html',)

def cargaArchivos(request):
    return render(request, 'cargaArchivos.html')



