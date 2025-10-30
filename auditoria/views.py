from django.shortcuts import render,redirect
from usuarios.models import Usuario
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReporteForm


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
    usuario_id = request.session.get('usuario_id')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        data = {'Usuario': usuario}
        return render(request, 'configuracion.html', data)
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado")
        return redirect('iniciarSesion')

def ConfiguraciónAdmin(request):
    usuario_id = request.session.get('usuario_id')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        data = {'Usuario': usuario}
        return render(request, 'configuracionAdmin.html', data)
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado")
    return redirect('iniciarSesion')

def verificacionUsuario(request):
    return render(request,"Verificacion.html")

def reportes(request):
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            usuario = Usuario.objects.get(id = request.session['usuario_id'])
            reporte.usuario = usuario
            messages.success(request, 'Reporte exitoso')
            return redirect("Reportes")
        else:
            messages.error(request, 'Error al enviar el reporte')
        return redirect("Reportes")    
    else:
        form = ReporteForm()
        return render(request, 'Reportes.html', {'form': form})

def cargaArchivos(request):
    return render(request, 'cargaArchivos.html')



