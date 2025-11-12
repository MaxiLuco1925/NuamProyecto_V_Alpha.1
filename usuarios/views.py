from django.shortcuts import render, redirect, get_object_or_404
from usuarios.forms import RegisterForm, InicioSesionForm
from django.contrib import messages
from usuarios.models import Usuario
import yfinance as yf
from declaraciones.forms import EditarCalificacionForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from auditoria.models import Instrumento
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout
from usuarios.forms import UsuarioRolForm
from auditoria.models import CalificacionTributaria
from declaraciones.forms import IngresoCalificacionManualForm
from instrumentos.models import Mercado
from django.conf import settings
import requests
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import json
from django.http import HttpResponse
import csv

def portada(request):
    return render(request, "index.html")

def registro(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.region = request.POST.get('region')
            usuario.comuna = request.POST.get('comuna')
            usuario.save()
            messages.success(request, 'Registro exitoso')
            return redirect('iniciarSesion')
        else:
            return render(request, 'registro.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'registro.html', {'form': form})

def iniciarSesion(request):
    if request.method == 'POST':
        form = InicioSesionForm(request.POST)
        if form.is_valid():
            documento = form.cleaned_data["documento_identidad"]
            contraseña = form.cleaned_data["contraseña"]
            try:
                usuario = Usuario.objects.get(documento_identidad=documento)
            except Usuario.DoesNotExist:
                messages.error(request, "Documento no existe")
                return render(request, 'InicioSesion.html', {'form': form})
            
            if check_password(contraseña, usuario.contraseña_hash):
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.nombre
                request.session['usuario_documento'] = usuario.documento_identidad
                request.session.modified = True 
               

                if usuario.rol and usuario.rol.descripcion == "Administrador":
                    return redirect("interfazAdmin")
                else:
                    return redirect("interfazinicio")
            else:
                messages.error(request, "Contraseña incorrecta")
                return render(request, 'InicioSesion.html', {'form': form})
        else:
            messages.error(request, "Credenciales inválidas")
            return render(request, 'InicioSesion.html', {'form': form})
    else:
        form = InicioSesionForm()
        return render(request, 'InicioSesion.html', {'form': form})


def interfazinicio(request):
    usuario_id = request.session.get('usuario_id')
    
    if not usuario_id:
        messages.error(request, "Debes iniciar sesión primero")
        return redirect('iniciarSesion')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        context = {
            'Usuario': usuario
        }
        return render(request, "interfazinicio.html", context)
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado")
        return redirect('iniciarSesion')

@require_http_methods(["GET"])
def market_data_api(request):
    indices = {
        "America": ["^IXIC", "^NDX", "^GSPC"],
        "Europe": ["^OMX", "^STOXX50E", "^FTSE"]
    }

    symbol_names = {
        ".IXIC": "COMP",
        ".NDX": "NDX",
        "^GSPC": "SPX",
        "^OMX": "OMXN40",
        "^STOXX50E": "STOXX50",
        "^FTSE": "FTSE"
    }

    result = {"America": [], "Europe": []}

    for region, symbols in indices.items():
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")

                if len(hist) < 2:
                    hist = ticker.history(period="1d")
                    if hist.empty:
                        continue
                    last_price = hist['Close'].iloc[-1]
                    prev_close = last_price
                else:
                    last_price = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2]

                change_abs = last_price - prev_close
                change_pct = (change_abs / prev_close) * 100 if prev_close != 0 else 0

                result[region].append({
                    "symbol": symbol_names.get(symbol, symbol),
                    "last": round(last_price, 2),
                    "change_abs": round(change_abs, 2),
                    "change_pct": round(change_pct, 2)
                })

            except Exception as e:
                print(f"Error al obtener {symbol}: {e}")
                continue

    return JsonResponse(result)

def Administrador(request):
    if 'usuario_id' not in request.session:
        return redirect('iniciarSesion')
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'])
        if not usuario.rol or usuario.rol.descripcion != "Administrador":
            messages.error(request, "Debes ser Administrador !!!")
            return redirect('interfazAdmin')
    except Usuario.DoesNotExist:
        return redirect('iniciarSesion')
    
    return render(request, 'interfazAdministrador.html')

def panel(request):
    usuario = Usuario.objects.filter(id=request.session.get('usuario_id')).first()
    
    if not usuario:
        return redirect('iniciarSesion')  
    mercados = Mercado.objects.all()
    
    calificaciones = CalificacionTributaria.objects.select_related(
        'instrumento', 'declaracion', 'usuario'
    ).prefetch_related(
        'factormensual_set'
    ).order_by('-fecha_pago')

    
    mercado = request.GET.get('mercado')
    instrumento = request.GET.get('instrumento')
    año = request.GET.get('año')

    if mercado:
        calificaciones = calificaciones.filter(instrumento__mercado=mercado)
    if instrumento:
        calificaciones = calificaciones.filter(instrumento__id=instrumento)
    if año:
        calificaciones = calificaciones.filter(año_tributario=año)

    return render(request, 'panelCalificacion.html', {
        'calificaciones': calificaciones,  
        'instrumentos': Instrumento.objects.all(),
        'años': CalificacionTributaria.objects.values_list('año_tributario', flat=True).distinct().order_by('año_tributario'),
        'usuario': usuario, 
        'mercados' : mercados
         
    })



def panelAdmin(request):
    usuario = Usuario.objects.filter(id=request.session.get('usuario_id')).first()
    
    if not usuario:
        return redirect('iniciarSesion')  
    mercados = Mercado.objects.all()
    
    calificaciones = CalificacionTributaria.objects.select_related(
        'instrumento', 'declaracion', 'usuario'
    ).prefetch_related(
        'factormensual_set'
    ).order_by('-fecha_pago')

    
    mercado = request.GET.get('mercado')
    instrumento = request.GET.get('instrumento')
    año = request.GET.get('año')

    if mercado:
        calificaciones = calificaciones.filter(instrumento__mercado=mercado)
    if instrumento:
        calificaciones = calificaciones.filter(instrumento__id=instrumento)
    if año:
        calificaciones = calificaciones.filter(año_tributario=año)

    return render(request, 'panelCalificacionAdmin.html', {
        'calificaciones': calificaciones,  
        'instrumentos': Instrumento.objects.all(),
        'años': CalificacionTributaria.objects.values_list('año_tributario', flat=True).distinct().order_by('año_tributario'),
        'usuario': usuario, 
        'mercados' : mercados
         
    })
                                                  
def listausuarios(request):                                               
    usuarios = Usuario.objects.select_related('rol').order_by('nombre')  
    return render(request, 'adminlista.html', {'usuarios': usuarios})    

def EditarRolusuario(request, pk):
    usuario = get_object_or_404(Usuario, pk = pk)
    if request.method == 'POST':
        form = UsuarioRolForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Rol actualizado correctamente.")
            return redirect('listausuarios')
        else:
            messages.error(request, "Error al actualizar el rol.")
    else:
        form = UsuarioRolForm(instance=usuario)
    
    return render(request, 'adminEditarRoles.html', {'form': form, 'usuario': usuario}) 

                                                   
def adminEliminarUsuario(request, pk):                                   
    try:
        usuario = Usuario.objects.get(pk=pk)                               
    except Usuario.DoesNotExist:                                        
        messages.error(request, "El usuario no existe.")                   
        return redirect('listausuarios')                                  

    if request.method == 'POST':
        usuario.delete()                                         
        messages.success(request, "Usuario eliminado correctamente.")    
        return redirect('listausuarios')                               

    return render(request, 'adminDeleteUser.html', {'usuario': usuario})



def salir(request):
    request.session.flush()
    return redirect('iniciarSesion')

def descargar_calificacion(request, calificacion_id):
    calificacion = CalificacionTributaria.objects.get(id=calificacion_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="calificacion_{calificacion_id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 2*cm

    p.setFont("Helvetica-Bold", 16)
    p.drawString(2*cm, y, f"Calificación Tributaria N° {calificacion.id}")
    y -= 1.5*cm

    p.setFont("Helvetica", 11)
    p.drawString(2*cm, y, f"Responsable: {calificacion.usuario.nombre}")
    y -= 0.6*cm
    p.drawString(2*cm, y, f"Instrumento: {calificacion.instrumento.nombre if calificacion.instrumento else '-'}")
    y -= 0.6*cm
    p.drawString(2*cm, y, f"Año Tributario: {calificacion.año_tributario}")
    y -= 0.6*cm
    p.drawString(2*cm, y, f"Fecha de Pago: {calificacion.fecha_pago.strftime('%d/%m/%Y %H:%M')}")
    y -= 0.6*cm
    p.drawString(2*cm, y, f"Descripción: {calificacion.descripcion[:90]}...")
    y -= 0.6*cm
    p.drawString(2*cm, y, f"Secuencia: {calificacion.secuencia_evento}")
    y -= 0.6*cm
    p.drawString(2*cm, y, f"Dividendo: ${calificacion.dividendo:,.2f}")
    y -= 0.6*cm
    p.drawString(2*cm, y, f"Valor Histórico: ${calificacion.valor_historico:,.2f}")
    y -= 0.6*cm
    p.drawString(2*cm, y, f"ISFUT: {'Sí' if calificacion.isfut else 'No'}")
    y -= 0.6*cm
    p.drawString(2*cm, y, f"Estado: {calificacion.estado_tributario}")
    y -= 1*cm


    p.setFont("Helvetica-Bold", 12)
    p.drawString(2*cm, y, "Factores Mensuales:")
    y -= 0.8*cm
    p.setFont("Helvetica", 10)

    factores = calificacion.factormensual_set.all().order_by("numero_factor")
    for f in factores:
        texto = f"Factor-{f.numero_factor:02d}: {f.valor_factor:.2f} ({f.descripcion})"
        p.drawString(2.5*cm, y, texto)
        y -= 0.5*cm
        if y < 2*cm:  
            p.showPage()
            p.setFont("Helvetica", 10)
            y = height - 2*cm

    p.showPage()
    p.save()
    return response

def ver_detalle_calificacion(request, calificacion_id):
    calificacion = get_object_or_404(CalificacionTributaria, id=calificacion_id)
    factores = calificacion.factormensual_set.all().order_by("numero_factor")
    return render(request, 'ver_detalle_calificacion.html', {
        'calificacion': calificacion,
        'factores': factores
    })




def editar_calificacion_manual(request, pk):
    calificacion = get_object_or_404(CalificacionTributaria, pk=pk)
    
    if request.method == 'POST':
        form = EditarCalificacionForm(request.POST, instance=calificacion)
        if form.is_valid():
            form.save()
            return redirect('panelCalificacion')
        else:
            messages.error(request, "Error al actualizar la calificación.")
    else:
        form = EditarCalificacionForm(instance=calificacion)

    return render(request, 'CalificacionManul.html', {'form': form, 'calificacion': calificacion})
