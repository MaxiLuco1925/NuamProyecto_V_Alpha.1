from django.shortcuts import render, redirect, get_object_or_404
from usuarios.forms import RegisterForm, InicioSesionForm, ResetearContraseñaForm
from django.contrib import messages
from usuarios.models import Usuario, AuditoriaSesion
import yfinance as yf
from django.core.mail import send_mail
from django.conf import settings
from auditoria.forms import CargaArchivoForm
from auditoria.models import CargaArchivo
import random
from declaraciones.forms import EditarCalificacionForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from auditoria.models import Instrumento
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout, get_user_model
from usuarios.forms import UsuarioRolForm
from auditoria.models import CalificacionTributaria
from declaraciones.forms import IngresoCalificacionManualForm
from instrumentos.models import Mercado
from django.conf import settings
import requests
import os
from django.db.models import Prefetch
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import json
from django.http import HttpResponse
import csv
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

def portada(request):
    return render(request, "index.html")

def asignaRol(*roles):
    def decorador(view_func):
        def wrapper(request, *args, **kwargs):
            usuario_id = request.session.get('usuario_id')

            if not usuario_id:
                messages.error(request, "Debes iniciar sesión primero.")
                return redirect('iniciarSesion')

            try:
                usuario = Usuario.objects.get(id=usuario_id)
            except Usuario.DoesNotExist:
                messages.error(request, "Usuario no encontrado.")
                return redirect('iniciarSesion')


            if not usuario.rol:
                messages.error(request, "No tienes permisos para acceder.")
                return redirect('interfazinicio')

            if usuario.rol.descripcion not in roles:
                messages.error(request, "No tienes permisos para esta sección.")
                return redirect('interfazinicio')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorador

               
@csrf_protect
def registro(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.region = request.POST.get('region')
            usuario.comuna = request.POST.get('comuna')
            usuario.verificado = False 
            usuario.save()

            codigo = random.randint(100000, 999999)
            request.session['codigo_verificacion'] = str(codigo)
            request.session['usuario_id'] = usuario.id
            print('EMAIL:', usuario.email)
            print('DEFAULT_FROM_EMAIL:', settings.DEFAULT_FROM_EMAIL)
            print('EMAIL_HOST_USER:', settings.EMAIL_HOST_USER)
            try:
                send_mail(
                    subject='Código de verificación NUAM',
                    message=f'Tu código de verificación es: {codigo}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[usuario.email],
                    fail_silently=False,
                )
                messages.info(request, f"Se envió un código de verificación a {usuario.email}")
            except Exception as e:
                messages.error(request, f"Error al enviar correo: {e}")

            return redirect('verificacion') 
        else:
            return render(request, 'registro.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'registro.html', {'form': form})
@csrf_protect
def iniciarSesion(request):
    if request.method == 'POST':
        form = InicioSesionForm(request.POST)
        if form.is_valid():
            documento = form.cleaned_data["documento_identidad"]
            contraseña = form.cleaned_data["contraseña"]

            try:
                usuario = Usuario.objects.get(documento_identidad=documento)
            except Usuario.DoesNotExist:
                AuditoriaSesion.objects.create(
                    usuario = None,
                    documento_intentado = documento,
                    exito = False,
                    rol=""
                )
                messages.error(request, " El Documento no existe.")
                return render(request, 'InicioSesion.html', {'form': form})

            if check_password(contraseña, usuario.contraseña_hash):
                AuditoriaSesion.objects.create(
                    usuario = usuario,
                    documento_intentado=documento,
                    exito = True,
                    rol = usuario.rol.descripcion if usuario.rol else "Sin rol"
                )

                if not usuario.verificado:
                    messages.warning(request, "Debes verificar Primero tu correo antes de iniciar sesión.")
                    return redirect('verificacion')

                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.nombre
                request.session['usuario_documento'] = usuario.documento_identidad

                if usuario.rol and usuario.rol.descripcion == "Administrador":
                    return redirect("interfazAdmin")  
                
                return redirect("interfazinicio")

            else:
                AuditoriaSesion.objects.create(
                    usuario = usuario,
                    documento_intentado = documento,
                    exito = False,
                    rol = usuario.rol.descripcion if usuario.rol else "Sin rol"
                )
                messages.error(request, " Contraseña incorrecta.")
        else:
            messages.error(request, " Credenciales inválidas.")
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
        total_archivos = CargaArchivo.objects.filter(cargado_por=usuario).count()
        total_calificaciones = CalificacionTributaria.objects.filter(usuario=usuario).count()
        context = {
            'Usuario': usuario,
            'total_calificaciones': total_calificaciones,
            'total_archivos': total_archivos
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

@asignaRol("Administrador")
def Administrador(request):
    return render(request, 'interfazAdministrador.html')

@asignaRol("Corredor", "Administrador")

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
        # Si se selecciona "Instrumento no inscrito", filtrar calificaciones sin instrumento
        if instrumento == 'no_inscrito':
            calificaciones = calificaciones.filter(instrumento__isnull=True)
        else:
            calificaciones = calificaciones.filter(instrumento__id=instrumento)
    if año:
        calificaciones = calificaciones.filter(año_tributario=año)

    # Obtener instrumentos de la base de datos y agregar la opción "no inscrito"
    instrumentos_db = Instrumento.objects.all()
    
    # Crear lista de instrumentos que incluya la opción especial
    instrumentos_con_opcion = list(instrumentos_db)
    
    # Crear objeto ficticio para "Instrumento no inscrito"
    InstrumentoFicticio = type('InstrumentoFicticio', (), {})
    instrumento_no_inscrito = InstrumentoFicticio()
    instrumento_no_inscrito.id = 'no_inscrito'
    instrumento_no_inscrito.nombre = 'Instrumento no inscrito'
    
    # Agregar al inicio de la lista
    instrumentos_con_opcion.insert(0, instrumento_no_inscrito)

    return render(request, 'panelCalificacion.html', {
        'calificaciones': calificaciones,  
        'instrumentos': instrumentos_con_opcion,  # Usar la lista modificada
        'años': CalificacionTributaria.objects.values_list('año_tributario', flat=True).distinct().order_by('año_tributario'),
        'usuario': usuario, 
        'mercados' : mercados
    })


@asignaRol("Administrador")
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
@asignaRol("Administrador")                                                  
def listausuarios(request):                                               
    usuarios = Usuario.objects.select_related('rol').order_by('nombre')  
    return render(request, 'adminlista.html', {'usuarios': usuarios}) 
   
@asignaRol("Administrador")
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

@asignaRol("Administrador")                                                   
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

@asignaRol("Corredor", "Administrador")
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

@asignaRol("Corredor", "Administrador")
def ver_detalle_calificacion(request, calificacion_id):
    calificacion = get_object_or_404(CalificacionTributaria, id=calificacion_id)
    factores = calificacion.factormensual_set.all().order_by("numero_factor")
    return render(request, 'ver_detalle_calificacion.html', {
        'calificacion': calificacion,
        'factores': factores
    })



@asignaRol("Corredor", "Administrador")
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

    return render(request, 'CalificacionManual.html', {'form': form, 'calificacion': calificacion})

@asignaRol("Administrador")
def descargar_calificacion_Admin(request, calificacion_id):
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

@asignaRol("Administrador")
def ver_detalle_calificacion_Admin(request, calificacion_id):
    calificacion = get_object_or_404(CalificacionTributaria, id=calificacion_id)
    factores = calificacion.factormensual_set.all().order_by("numero_factor")
    return render(request, 'ver_detalles_calificacion_admin.html', {
        'calificacion': calificacion,
        'factores': factores
    })



@asignaRol("Administrador")
def editar_calificacion_manual_Admin(request, pk):
    calificacion = get_object_or_404(CalificacionTributaria, pk=pk)
    
    if request.method == 'POST':
        form = EditarCalificacionForm(request.POST, instance=calificacion)
        if form.is_valid():
            form.save()
            return redirect('panelCalificacionAdmin')
        else:
            messages.error(request, "Error al actualizar la calificación.")
    else:
        form = EditarCalificacionForm(instance=calificacion)

    return render(request, 'CalificacionManualAdmin.html', {'form': form, 'calificacion': calificacion})



@asignaRol("Administrador")
def eliminar_calificacion(request, pk):
    calificacion = get_object_or_404(CalificacionTributaria, pk=pk)
    calificacion.delete()
    messages.success(request, "Calificación eliminada correctamente.")
    return redirect('panelCalificacionAdmin')




def verificar_codigo(request):
    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo')
        codigo_correcto = str(request.session.get('codigo_verificacion'))
        usuario_id = request.session.get('usuario_id')

        if codigo_ingresado == codigo_correcto and usuario_id:
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                usuario.verificado = True 
                usuario.save()

                request.session.pop('codigo_verificacion', None)
                messages.success(request, " Verificación exitosa. Ahora puedes iniciar sesión.")
                return redirect('iniciarSesion')
            except Usuario.DoesNotExist:
                messages.error(request, " Usuario no encontrado.")
        else:
            messages.error(request, " Código incorrecto. Intenta nuevamente.")

    return render(request, 'Verificacion.html')



def auditoriaSesiones(request):
    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        messages.error(request, "Debes iniciar sesión primero.")
        return redirect("iniciarSesion")


    usuario = Usuario.objects.filter(id=usuario_id).first()


    if not usuario or not usuario.rol or usuario.rol.descripcion != "Administrador":
        messages.error(request, "No tienes permiso para acceder a auditorías.")
        return redirect("interfazinicio")


    auditorias = AuditoriaSesion.objects.select_related("usuario").order_by("-fecha")

    return render(request, "auditoriaSesiones.html", {"auditorias": auditorias})


@asignaRol("Corredor", "Administrador")
def panelArchivoXFactor(request):
    usuario = Usuario.objects.filter(id=request.session.get('usuario_id')).first()
    if not usuario:
        return redirect('iniciarSesion')

    mercados = Mercado.objects.all()
    instrumentos = Instrumento.objects.all()
    años = CalificacionTributaria.objects.values_list(
        'año_tributario', flat=True
    ).distinct().order_by("año_tributario")

    calificaciones = CalificacionTributaria.objects.select_related(
        "instrumento", "usuario"
    ).prefetch_related(
        "factormensual_set"
    ).filter(
        origen__cargado_por=usuario
    ).order_by("-fecha_pago")

    mercado = request.GET.get("mercado")
    instrumento = request.GET.get("instrumento")
    año = request.GET.get("año")

    if mercado:
        calificaciones = calificaciones.filter(instrumento__mercado=mercado)
    if instrumento:
        calificaciones = calificaciones.filter(instrumento__id=instrumento)
    if año:
        calificaciones = calificaciones.filter(año_tributario=año)

    return render(request, "archivo_x_factor.html", {
        "usuario": usuario,
        "calificaciones": calificaciones,
        "instrumentos": instrumentos,
        "mercados": mercados,
        "años": años,
        "rango_factores": list(range(8, 38)),
        "form": CargaArchivoForm(initial={"tipo_carga": "factores"}),
        "carga": None
    })





@asignaRol("Administrador")
def panelArchivoXFactorAdmin(request):
    usuario = Usuario.objects.filter(id=request.session.get('usuario_id')).first()
    if not usuario:
        return redirect('iniciarSesion')

    mercados = Mercado.objects.all()
    instrumentos = Instrumento.objects.all()
    años = CalificacionTributaria.objects.values_list(
        'año_tributario', flat=True
    ).distinct().order_by("año_tributario")

    calificaciones = CalificacionTributaria.objects.select_related(
        "instrumento", "usuario"
    ).prefetch_related(
        "factormensual_set"
    ).filter(
        origen__cargado_por=usuario
    ).order_by("-fecha_pago")

    mercado = request.GET.get("mercado")
    instrumento = request.GET.get("instrumento")
    año = request.GET.get("año")

    if mercado:
        calificaciones = calificaciones.filter(instrumento__mercado=mercado)
    if instrumento:
        calificaciones = calificaciones.filter(instrumento__id=instrumento)
    if año:
        calificaciones = calificaciones.filter(año_tributario=año)

    return render(request, "archivo_x_factorAdmin.html", {
        "usuario": usuario,
        "calificaciones": calificaciones,
        "instrumentos": instrumentos,
        "mercados": mercados,
        "años": años,
        "rango_factores": list(range(8, 38)),
        "form": CargaArchivoForm(initial={"tipo_carga": "factores"}),
        "carga": None
    })









