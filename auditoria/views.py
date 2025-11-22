from django.shortcuts import render,redirect
from usuarios.models import Usuario
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReporteForm
from auditoria.models import Reportes, AuditoriaLog
from django.http import JsonResponse
from usuarios.views import asignaRol

@asignaRol ("Corredor", "Administrador")
def x_factor(request):
    return render(request, 'archivo_x_factor.html')

@asignaRol ("Corredor", "Administrador")
def x_monto(request):
    return render(request, 'archivo_x_monto.html')

@asignaRol ("Administrador")
def x_factor_Admin(request):
    return render(request, 'archivo_x_factorAdmin.html')

@asignaRol("Administrador")
def x_monto_Admin(request):
    return render(request, 'archivo_x_montoAdmin.html' )

@asignaRol("Administrador")
def listadoUsuario(request):
    usuarios = Usuario.objects.all()
    data = {'usuarios' : usuarios}
    return render(request, 'listadoUsuario.html', data)


@asignaRol("Administrador")
def lecturaReportes(request):
    reportes = Reportes.objects.all()
    data = {'reportes' : reportes}
    return render(request, 'lecturaReportes.html', data)


@asignaRol("Administrador")
def revisado(request, reporte_id):
    if request.method == 'POST':
        reporte = Reportes.objects.get(id = reporte_id) 
        reporte.estado = "Revisado"
        reporte.save()
        return JsonResponse({'success' : True})
    
    
@asignaRol("Corredor", "Administrador")
def Factor(request):
    factores = range(8, 38)
    contexto = {'factores': factores}
    return render(request,'FactorImpuestos.html',contexto)

@asignaRol("Administrador")
def FactorAdmin(request):
    factores = range(8, 38)
    contexto = {'factores': factores}
    return render(request,'FactorImpuestosAdmin.html',contexto)


def Configuración(request):
    usuario_id = request.session.get('usuario_id')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        data = {'Usuario': usuario}
        return render(request, 'configuracion.html', data)
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado")
        return redirect('iniciarSesion')
    

@asignaRol("Administrador")
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


@asignaRol("Corredor")
def reportes(request):
    if request.method == 'POST':
        form = ReporteForm(request.POST, request.FILES)  # Agregado request.FILES
        if form.is_valid():
            try:
                reporte = form.save(commit=False)
                usuario = Usuario.objects.get(id=request.session['usuario_id'])
                reporte.usuario = usuario
                reporte.save()
                messages.success(request, 'Reporte creado exitosamente')
                return redirect("Reportes")
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuario no encontrado')
                return redirect('iniciarSesion')
            except Exception as e:
                messages.error(request, f'Error al enviar el reporte: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario')
            return render(request, 'Reportes.html', {'form': form})
    else:
        form = ReporteForm()
    
    return render(request, 'Reportes.html', {'form': form})

def cargaArchivos(request):
    return render(request, 'cargaArchivos.html')



@asignaRol("Administrador")
def auditoria_seguridad(request):
    registros = AuditoriaLog.objects.all().order_by('-fecha')#el "-" es para ordenar sin el guion es para ordenar desde el mas antiguo al mas nuevo y con es al reves
    return render(request, 'auditoria_seguridad.html', {'registros': registros})
