from django.shortcuts import render


def x_factor(request):
    return render(request, 'archivo_x_factor.html')

def x_monto(request):
    return render(request, 'archivo_x_monto.html')

def x_factor_Admin(request):
    return render(request, 'archivo_x_factorAdmin.html')

def x_monto_Admin(request):
    return render(request, 'archivo_x_montoAdmin.html' )

def listadoUsuario(request):
    return render(request, 'listadoUsuario.html')

def lecturaReportes(request):
    return render(request, 'lecturaReportes.html')

def Factor(request):
    factores = range(8, 38)
    contexto = {'factores': factores}
    return render(request,'FactorImpuestos.html',contexto)

def Configuración(request):
    return render(request, 'configuracion.html')

def ConfiguraciónAdmin(request):
    return render(request, 'configuracionAdmin.html')

def verificacionUsuario(request):
    return render(request,"Verificacion.html")

def reportes(request):
    return render(request,'Reportes.html',)



