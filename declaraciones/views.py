
from django.shortcuts import render, redirect
from . import forms
from django.contrib import messages
from usuarios.models import Usuario
from declaraciones.forms import IngresoCalificacionManualForm    

# Create your views here.
def ingresarCalificacion(request):
    form = forms.IngresoCalificacionManualForm()
    if request.method == 'POST':
        form = forms.IngresoCalificacionManualForm(request.POST)
        if form.is_valid():
            form.save(user = request.user)
            return redirect('panelCalificacion')
    else:
        form = IngresoCalificacionManualForm()     
    return render(request, 'CalificacionManul.html', {'form' : form})



