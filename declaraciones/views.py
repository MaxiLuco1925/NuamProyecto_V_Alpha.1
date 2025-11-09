
from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib import messages
from usuarios.models import Usuario
from auditoria.models import Instrumento, CalificacionTributaria
from declaraciones.forms import IngresoCalificacionManualForm, factoresForm
from auditoria.models import FactorMensual
from decimal import Decimal, ROUND_HALF_UP    
from django.http import JsonResponse
from django.utils import timezone

def ingresarCalificacion(request):
    if request.method == 'POST':
        form = forms.IngresoCalificacionManualForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            usuario_id = request.session.get('usuario_id')
            usuario = Usuario.objects.get(id=usuario_id)
            calificacion.instrumento = form.cleaned_data['instrumento']
            calificacion.usuario = usuario
            calificacion.save()
            
            request.session['calificacion_id'] = calificacion.id
            return redirect('factorListado')
    else:
        form = forms.IngresoCalificacionManualForm()
    return render(request, 'CalificacionManul.html', {'form': form})



def x_factorCalculo(request):
    calificacion_id = request.session.get('calificacion_id')
    
    if not calificacion_id:
        messages.error(request, 'No hay calificación activa.')
        return redirect('ingresarCalificacion')
    
    try:
        calificacion = CalificacionTributaria.objects.select_related('instrumento', 'usuario').get(id=calificacion_id)
    except CalificacionTributaria.DoesNotExist:
        messages.error(request, 'La calificación no existe.')
        if 'calificacion_id' in request.session:
            del request.session['calificacion_id']
        return redirect('ingresarCalificacion')
    
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')
        usuario = Usuario.objects.get(id=usuario_id)
        
        factores_nombres = {
            "factor_8": "No Constitutiva de Renta No Acogido a Impto",
            "factor_9": "Impuesto 1ra Categ. Afecto GL Comp. Con Devolución",
            "factor_10": "Impuesto Tasa Adicional Evento Art. 21",
            "factor_11": "Incremento Impuesto 1ra Categoría",
            "factor_12": "Impuesto 1ra Categ. Evento GL Comp. Con Devolución",
            "factor_13": "Ingresos afectados a GI con derecho a compensación sin devolución",
            "factor_14": "Ingresos Extentos de GI con derecho a compensasión sin devolución",
            "factor_15": "Ingresos sujetos a crédito por impuestos internos",
            "factor_16": "Ingresos no constitutivos de renta acogidos a impuesto",
            "factor_17": "Ingresos que consideran devolución de capital no constitutiva de renta",
            "factor_18": "Ingresos que se consideran exentos de IGC y/o IA",
            "factor_19": "Ingresos no constitutivos de Renta",
            "factor_20": "Ingresos con crédito sin derecho a devolución",
            "factor_21": "Ingresos con derecho a devolución",
            "factor_22": "Ingresos sin derecho a devolución ni imputación directa",
            "factor_23": "Ingresos con derecho a devolución",
            "factor_24": "Ingresos con crédito sin derecho a devolución",
            "factor_25": "Ingresos con derecho a devolución",
            "factor_26": "Sin derecho a devolución",
            "factor_27": "Con derecho a devolución",
            "factor_28": "Crédito por IPE",
            "factor_29": "Sin derecho a devolución",
            "factor_30": "Con derecho a devolución",
            "factor_31": "Sin derecho a devolución",
            "factor_32": "Con derecho a devolución",
            "factor_33": "Crédito por IPE",
            "factor_34": "Crédito por impto. Tasa adicional, Ex art 21 LIE",
            "factor_35": "Tasa efectiva del Crédito del FUT (TEF)",
            "factor_36": "Tasa Efectiva del Crédito del FUNT (TEX)",
            "factor_37": "Devolución de Capital Art. 17 num 7 LIR"
        }
        
        factores_creados = 0
        for key, descripcion in factores_nombres.items():
            valor = float(request.POST.get(key, 0) or 0)
            numero = int(key.split('_')[1]) 
            
            if valor != 0:
                FactorMensual.objects.create(
                    calificacion=calificacion,
                    usuario=usuario,
                    descripcion=descripcion,
                    valor_factor=valor,
                    fecha_factor=timezone.now(),
                    numero_factor=numero 
                )
                factores_creados += 1
        
        del request.session['calificacion_id']
        messages.success(request, f'Calificación guardada con {factores_creados} factores.')
        return redirect('panelCalificacion')
    
    context = {
        'calificacion': calificacion,
        'rango_montos': range(1, 38)
    }
    return render(request, 'factores.html', context)


            





