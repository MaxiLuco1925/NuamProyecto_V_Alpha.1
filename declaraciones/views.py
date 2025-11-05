
from django.shortcuts import render, redirect
from . import forms
from django.contrib import messages
from usuarios.models import Usuario
from declaraciones.forms import IngresoCalificacionManualForm, factoresForm
from auditoria.models import FactorMensual    

# Create your views here.
def ingresarCalificacion(request):
    if request.method == 'POST':
        form = forms.IngresoCalificacionManualForm(request.POST)
        if form.is_valid():
            form.save(user = request.user)
            return redirect('panelCalificacion')
    else:
        form = IngresoCalificacionManualForm()     
    return render(request, 'CalificacionManul.html', {'form' : form})


def listadoFactores(request):
    factores = FactorMensual.objects.all()
    data = {'factores' : factores}
    return render(request, 'factores.html', data)


def agregarFactor(request):
    if request.method == 'POST':
        form = factoresForm(request.POST)
        if form.is_valid():
            try:
                usuario_id = request.session.get('usuario_id')
                if not usuario_id:
                    messages.error(request, "Primero debes iniciar sesión para registrar un factor")
                    return redirect('iniciarSesion')
                usuario = Usuario.objects.get(id = usuario_id)

                factor = form.save(commit=False)
                factor.usuario = usuario
                form.save()

                messages.success(request, 'El factor se ha registrado correctamente')
                return redirect('listadoFactores')
            except Usuario.DoesNotExist:
                messages.error(request, "Usuario no encontrador, por favor inicia sesion ")
                return redirect('iniciarSesion')
        else:
            messages.error(request, 'Error al registrar el Factor. Verifica los datos ingresados!!.')
    else:
        form = factoresForm()

    return render(request, 'agregarFactores.html', {'form' : form}) 
           

                


def actualizarFactor(request, id):
    factores = FactorMensual.objects.get(id = id)
    form = factoresForm(instance=factores)
    if request.method == 'POST' :
        form = factoresForm(request.POST, instance=factores)
        if form.is_valid():
            form.save()
        return redirect('panelCalificacion')
    data = {'form' : form}
    return render(request, 'calcularFactores.html', data)    




