from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from . import forms
import io
from django.contrib import messages
from usuarios.models import Usuario
from auditoria.models import Instrumento, CalificacionTributaria
from declaraciones.forms import IngresoCalificacionManualForm
from auditoria.models import FactorMensual
from decimal import Decimal, ROUND_HALF_UP    
from django.http import JsonResponse
from django.utils import timezone
import csv
from decimal import Decimal, InvalidOperation
from django.utils.dateparse import parse_date
from auditoria.forms import CargaArchivoForm
from declaraciones.models import CargaArchivo
from usuarios.views import asignaRol
from instrumentos.models import Mercado

@asignaRol("Corredor")
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
    return render(request, 'CalificacionManual.html', {'form': form})


@asignaRol("Corredor", "Administrador")
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

            FactorMensual.objects.update_or_create(
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


@asignaRol("Administrador")           
def ingresarCalificacionAdmin(request):
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
    return render(request, 'CalificacionManualAdmin.html', {'form': form})

@asignaRol("Administrador")
def x_factorCalculoAdmin(request):
    calificacion_id = request.session.get('calificacion_id')
    
    if not calificacion_id:
        messages.error(request, 'No hay calificación activa.')
        return redirect('CalificacionManualAdmin')
    
    try:
        calificacion = CalificacionTributaria.objects.select_related('instrumento', 'usuario').get(id=calificacion_id)
    except CalificacionTributaria.DoesNotExist:
        messages.error(request, 'La calificación no existe.')
        if 'calificacion_id' in request.session:
            del request.session['calificacion_id']
        return redirect('CalificacionManualAdmin')
    
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

            FactorMensual.objects.update_or_create(
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
        return redirect('panelCalificacionAdmin')
    
    context = {
        'calificacion': calificacion,
        'rango_montos': range(1, 38)
    }
    return render(request, 'factoresAdmin.html', context)




def ProcesarArchivoCSV(archivo, tipo_carga, usuario, carga_origen):
    """
    Procesa CSV tolerante y registra errores en carga_origen.
    """
    texto = None
    try:
        contenido = archivo.read()
        if isinstance(contenido, bytes):
            texto = contenido.decode('utf-8-sig')
        else:
            texto = str(contenido)
        archivo.seek(0) 
    except Exception as e:
        carga_origen.mensaje_error = f"Error leyendo archivo: {e}"
        carga_origen.estado = 'fallida'
        carga_origen.save()
        return []

    stream = io.StringIO(texto)
    reader = csv.DictReader(stream)

    errores = []
    total = 0
    exitosos = 0
    calificaciones_creadas = []

    header = reader.fieldnames or []
    if not header:
        carga_origen.mensaje_error = "CSV sin encabezados detectables."
        carga_origen.estado = 'fallida'
        carga_origen.save()
        return []

    for fila in reader:
        total += 1
        try:
            instrumento_val = (fila.get('Instrumento') or
                            fila.get('instrumento') or
                            fila.get('codigo_instrumento') or
                            fila.get('codigo') or
                            fila.get('Codigo') or
                            '').strip()

            if not instrumento_val:
                raise ValueError("Columna 'Instrumento' o 'codigo_instrumento' vacía en esta fila.")

            instrumento = None
            try:
                instrumento = Instrumento.objects.get(codigo__iexact=instrumento_val)
            except Instrumento.DoesNotExist:
                instrumento = Instrumento.objects.filter(nombre__iexact=instrumento_val).first()
                if not instrumento:
                    instrumento = Instrumento.objects.filter(nombre__icontains=instrumento_val).first()

            if not instrumento:
                raise ValueError(f"Instrumento '{instrumento_val}' no encontrado en la base de datos.")

            secuencia = int(fila.get('Secuencia') or fila.get('secuencia') or 0)
            ejercicio = int(fila.get('Ejercicio') or fila.get('ejercicio') or 0)
            from django.utils.dateparse import parse_date
            fecha_pago = parse_date(fila.get('Fecha') or fila.get('fecha') or '')
            descripcion = (fila.get('Descripcion') or fila.get('descripcion') or '').strip()

            def to_float_safe(s):
                if s is None:
                    return 0.0
                s = str(s).strip()
                if not s:
                    return 0.0
                s = s.replace(',', '.')
                try:
                    return float(s)
                except Exception:
                    raise ValueError(f"Valor numérico inválido: '{s}'")

            dividendo = to_float_safe(fila.get('Dividendo') or fila.get('dividendo'))
            valor_historico = to_float_safe(fila.get('Valor Historico') or fila.get('valor historico') or fila.get('valor_historico'))
            isfut_raw = (fila.get('ISFUT') or fila.get('isfut') or '').strip().lower()
            isfut = isfut_raw in ['si', 's', 'yes', 'y', 'true', '1']

            with transaction.atomic():
                calificacion, creada = CalificacionTributaria.objects.update_or_create(
                    instrumento=instrumento,
                    secuencia_evento=secuencia,
                    año_tributario=ejercicio,
                    usuario=usuario,
                    defaults={
                        'fecha_pago': fecha_pago,
                        'descripcion': descripcion,
                        'dividendo': dividendo,
                        'valor_historico': valor_historico,
                        'isfut': isfut,
                        'origen': carga_origen,
                        'estado_tributario': 'procesado'
                    }
                )

                calificaciones_creadas.append(calificacion)
                suma_factores = Decimal('0')
                suma_error = False

                for i in range(8, 38):
                    col = f'Factor {i}'
                    raw = (fila.get(col) or fila.get(col.lower()) or '0')
                    raw = str(raw).strip() or '0'
                    raw = raw.replace(',', '.')
                    try:
                        valor = Decimal(raw)
                    except InvalidOperation:
                        raise ValueError(f"Valor inválido en columna '{col}': '{raw}'")

                    if 8 <= i <= 19:
                        suma_factores += valor

                    FactorMensual.objects.update_or_create(
                        calificacion=calificacion,
                        numero_factor=i,
                        defaults={
                            'valor_factor': float(valor),
                            'fecha_factor': calificacion.fecha_pago or timezone.now(),
                            'usuario': usuario,
                            'carga_origen': carga_origen,
                            'descripcion': f'Factor {i}'
                        }
                    )

                if suma_factores > Decimal('1'):
                    errores.append(f"Fila {total}: suma factores 8-19 > 1 (suma={suma_factores}) para instrumento '{instrumento_val}'")
                    suma_error = True

                if not suma_error:
                    exitosos += 1

        except Exception as e:
            errores.append(f"Fila {total}: Instrumento '{instrumento_val}' -> {str(e)}")

    carga_origen.total_registros = total
    carga_origen.registros_exitosos = exitosos
    carga_origen.estado = (
        'completa' if exitosos == total and total > 0 else
        'fallida' if exitosos == 0 and total > 0 else
        'procesando'
    )
    carga_origen.mensaje_error = "\n".join(errores) if errores else None
    carga_origen.save()
    return calificaciones_creadas



@asignaRol("Corredor")
def carga_masiva_factores_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('iniciarSesion')

    usuario = Usuario.objects.filter(id=usuario_id).first()
    if not usuario:
        return redirect("iniciarSesion")

    calificaciones = []
    carga_origen = None

    if request.method == "POST":
        form = CargaArchivoForm(request.POST, request.FILES)

        if form.is_valid():
            archivo = request.FILES["archivo"]
            tipo_carga = form.cleaned_data["tipo_carga"]

            archivo.seek(0)
            carga_origen = CargaArchivo.objects.create(
                archivo=archivo,
                tipo_carga=tipo_carga,
                cargado_por=usuario,
                estado="procesando"
            )
            archivo.seek(0) 
            calificaciones = ProcesarArchivoCSV(
                archivo=archivo,
                tipo_carga=tipo_carga,
                usuario=usuario,
                carga_origen=carga_origen
            )
    else:
        form = CargaArchivoForm(initial={"tipo_carga": "factores"})

    return render(request, "archivo_x_factor.html", {
        "form": form,
        "calificaciones": calificaciones,
        "carga": carga_origen,
        "rango_factores": list(range(8, 38)),
    })


def ProcesarArchivoMontosCSV(archivo, tipo_carga, usuario, carga_origen):
    """
    Procesa CSV con montos y calcula automáticamente los factores 8-19.
    Crea instrumentos automáticamente si no existen, asignando el mercado correcto.
    """
    texto = None
    try:
        contenido = archivo.read()
        if isinstance(contenido, bytes):
            texto = contenido.decode('utf-8-sig')
        else:
            texto = str(contenido)
        archivo.seek(0)
    except Exception as e:
        carga_origen.mensaje_error = f"Error leyendo archivo: {e}"
        carga_origen.estado = 'fallida'
        carga_origen.save()
        return []

    stream = io.StringIO(texto)
    reader = csv.DictReader(stream)

    errores = []
    total = 0
    exitosos = 0
    calificaciones_creadas = []

    header = reader.fieldnames or []
    if not header:
        carga_origen.mensaje_error = "CSV sin encabezados detectables."
        carga_origen.estado = 'fallida'
        carga_origen.save()
        return []

    mercados_por_tipo = {
        'ACC': 'Acciones',
        'BON': 'Bonos', 
        'CRY': 'Criptomonedas',
        'FIN': 'Instrumentos financieros',
        'EXP': 'Exportaciones',
        'IMP': 'Importaciones',
        'SER': 'Servicios',
        'REN': 'Renta inmobiliaria',
        'COM': 'Comercio',
        'AGR': 'Agroindustria'
    }
    
    mercados_dict = {mercado.nombre: mercado for mercado in Mercado.objects.all()}
    if not mercados_dict:
        errores.append("No hay mercados configurados en el sistema")
        carga_origen.mensaje_error = "\n".join(errores)
        carga_origen.estado = 'fallida'
        carga_origen.save()
        return []

    for fila in reader:
        total += 1
        instrumento_val = None
        try:
            instrumento_val = (fila.get('Instrumento') or
                            fila.get('instrumento') or
                            fila.get('codigo_instrumento') or
                            fila.get('codigo') or
                            fila.get('Codigo') or
                            '').strip()

            if not instrumento_val:
                raise ValueError("Columna 'Instrumento' o 'codigo_instrumento' vacía en esta fila.")
            instrumento = None
            try:
                instrumento = Instrumento.objects.get(codigo__iexact=instrumento_val)
                print(f" Instrumento encontrado: {instrumento_val}")
            except Instrumento.DoesNotExist:
                mercado_asignado = None
                for prefijo, mercado_nombre in mercados_por_tipo.items():
                    if instrumento_val.startswith(prefijo):
                        mercado_asignado = mercados_dict.get(mercado_nombre)
                        break
                
                if not mercado_asignado:
                    mercado_asignado = list(mercados_dict.values())[0]
                
                tipo_instrumento = mercados_por_tipo.get(instrumento_val[:3], "Acción")
                instrumento = Instrumento.objects.create(
                    codigo=instrumento_val,
                    nombre=f"Instrumento {instrumento_val}",
                    mercado=mercado_asignado,
                    tipo_instrumento=tipo_instrumento
                )
                print(f" Instrumento creado: {instrumento_val} en mercado {mercado_asignado.nombre}")

            secuencia = int(fila.get('Secuencia') or fila.get('secuencia') or 0)
            ejercicio = int(fila.get('Ejercicio') or fila.get('ejercicio') or 0)
            
            from django.utils.dateparse import parse_date
            fecha_pago_str = fila.get('Fecha') or fila.get('fecha') or ''
            fecha_pago = parse_date(fecha_pago_str)
            if not fecha_pago:
                fecha_pago = timezone.now().date()
                
            descripcion = (fila.get('Descripcion') or fila.get('descripcion') or f"Dividendo {instrumento_val}").strip()

            def to_float_safe(s):
                if s is None:
                    return 0.0
                s = str(s).strip()
                if not s:
                    return 0.0
                s = s.replace(',', '.')
                try:
                    return float(s)
                except Exception:
                    raise ValueError(f"Valor numérico inválido: '{s}'")

            dividendo = to_float_safe(fila.get('Dividendo') or fila.get('dividendo'))
            valor_historico = to_float_safe(fila.get('Valor Historico') or fila.get('valor historico') or fila.get('valor_historico'))
            isfut_raw = (fila.get('ISFUT') or fila.get('isfut') or '').strip().lower()
            isfut = isfut_raw in ['si', 's', 'yes', 'y', 'true', '1']

            montos = {}
            total_montos = 0.0
            
            for i in range(1, 13):
                col_monto = f'Monto {i}'
                raw_monto = (fila.get(col_monto) or fila.get(col_monto.lower()) or '0')
                monto_valor = to_float_safe(raw_monto)
                montos[i] = monto_valor
                total_montos += monto_valor

            if total_montos == 0:
                raise ValueError("El total de los Montos ingresados es igual a 0. ¡No se puede calcular!")

            with transaction.atomic():
                calificacion, creada = CalificacionTributaria.objects.update_or_create(
                    instrumento=instrumento,
                    secuencia_evento=secuencia,
                    año_tributario=ejercicio,
                    usuario=usuario,
                    defaults={
                        'fecha_pago': fecha_pago,
                        'descripcion': descripcion,
                        'dividendo': dividendo,
                        'valor_historico': valor_historico,
                        'isfut': isfut,
                        'origen': carga_origen,
                        'estado_tributario': 'procesado'
                    }
                )

                calificaciones_creadas.append(calificacion)
                suma_factores = Decimal('0')

                for factor_num in range(8, 38):
                    calculo = Decimal('0')
                    
                    if 8 <= factor_num <= 19:
                        monto_index = factor_num - 7
                        monto_asociado = montos.get(monto_index, 0.0)
                        
                        if monto_asociado > 0 and total_montos > 0:
                            calculo = Decimal(str(monto_asociado)) / Decimal(str(total_montos))
                    
                    FactorMensual.objects.update_or_create(
                        calificacion=calificacion,
                        numero_factor=factor_num,
                        defaults={
                            'valor_factor': float(calculo),
                            'fecha_factor': fecha_pago,
                            'usuario': usuario,
                            'carga_origen': carga_origen,
                            'descripcion': f'Factor {factor_num}' + (f' (calculado desde Monto {monto_index})' if 8 <= factor_num <= 19 else '')
                        }
                    )
                    
                    if 8 <= factor_num <= 19:
                        suma_factores += calculo

                suma_redondeada = round(suma_factores, 6)
                if suma_redondeada > Decimal('1.000000'):
                    errores.append(f"Fila {total}: suma factores 8-19 = {suma_redondeada:.6f} > 1.000000 para instrumento '{instrumento_val}'")
                elif suma_redondeada < Decimal('0.999999'):
                    if suma_redondeada < Decimal('0.999000'):
                        errores.append(f"Fila {total}: suma factores 8-19 = {suma_redondeada:.6f} < 1.000000 para instrumento '{instrumento_val}'")
                    else:
                        exitosos += 1
                else:
                    exitosos += 1

        except Exception as e:
            if instrumento_val:
                errores.append(f"Fila {total}: Instrumento '{instrumento_val}' -> {str(e)}")
            else:
                errores.append(f"Fila {total}: Error -> {str(e)}")

    carga_origen.total_registros = total
    carga_origen.registros_exitosos = exitosos
    carga_origen.estado = (
        'completa' if exitosos == total and total > 0 else
        'fallida' if exitosos == 0 and total > 0 else
        'procesando'
    )
    carga_origen.mensaje_error = "\n".join(errores) if errores else None
    carga_origen.save()
    
    print(f" Procesamiento completado: {exitosos}/{total} registros exitosos")
    return calificaciones_creadas

@asignaRol("Corredor")

def carga_masiva_montos_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('iniciarSesion')

    usuario = Usuario.objects.filter(id=usuario_id).first()
    if not usuario:
        return redirect("iniciarSesion")

    calificaciones = []
    carga_origen = None

    if request.method == "POST":
        form = CargaArchivoForm(request.POST, request.FILES)
        
        if form.is_valid():
            archivo = request.FILES["archivo"]

            tipo_carga = 'montos:dj1948'
            
            archivo.seek(0)
            carga_origen = CargaArchivo.objects.create(
                archivo=archivo,
                tipo_carga=tipo_carga, 
                cargado_por=usuario,
                estado="procesando"
            )
            archivo.seek(0)
            calificaciones = ProcesarArchivoMontosCSV(
                archivo=archivo,
                tipo_carga=tipo_carga,
                usuario=usuario,
                carga_origen=carga_origen
            )
    else:
        form = CargaArchivoForm(initial={'tipo_carga': 'montos:dj1948'})

    return render(request, "archivo_x_montos.html", {
        "form": form,
        "calificaciones": calificaciones,
        "carga": carga_origen,
        "rango_montos": list(range(1, 30)),
        "rango_factores": list(range(8, 38)),
    })




@asignaRol("Administrador")
def carga_masiva_factores_Admin(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('iniciarSesion')

    usuario = Usuario.objects.filter(id=usuario_id).first()
    if not usuario:
        return redirect("iniciarSesion")

    calificaciones = []
    carga_origen = None

    if request.method == "POST":
        form = CargaArchivoForm(request.POST, request.FILES)

        if form.is_valid():
            archivo = request.FILES["archivo"]
            tipo_carga = form.cleaned_data["tipo_carga"]

            archivo.seek(0)
            carga_origen = CargaArchivo.objects.create(
                archivo=archivo,
                tipo_carga=tipo_carga,
                cargado_por=usuario,
                estado="procesando"
            )
            archivo.seek(0) 
            calificaciones = ProcesarArchivoCSV(
                archivo=archivo,
                tipo_carga=tipo_carga,
                usuario=usuario,
                carga_origen=carga_origen
            )
    else:
        form = CargaArchivoForm(initial={"tipo_carga": "factores"})

    return render(request, "archivo_x_factorAdmin.html", {
        "form": form,
        "calificaciones": calificaciones,
        "carga": carga_origen,
        "rango_factores": list(range(8, 38)),
    })



@asignaRol("Administrador")

def carga_masiva_montos_Admin(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('iniciarSesion')

    usuario = Usuario.objects.filter(id=usuario_id).first()
    if not usuario:
        return redirect("iniciarSesion")

    calificaciones = []
    carga_origen = None

    if request.method == "POST":
        form = CargaArchivoForm(request.POST, request.FILES)
        
        if form.is_valid():
            archivo = request.FILES["archivo"]

            tipo_carga = 'montos:dj1948'
            
            archivo.seek(0)
            carga_origen = CargaArchivo.objects.create(
                archivo=archivo,
                tipo_carga=tipo_carga, 
                cargado_por=usuario,
                estado="procesando"
            )
            archivo.seek(0)
            calificaciones = ProcesarArchivoMontosCSV(
                archivo=archivo,
                tipo_carga=tipo_carga,
                usuario=usuario,
                carga_origen=carga_origen
            )
    else:
        form = CargaArchivoForm(initial={'tipo_carga': 'montos:dj1948'})

    return render(request, "archivo_x_montoAdmin.html", {
        "form": form,
        "calificaciones": calificaciones,
        "carga": carga_origen,
        "rango_montos": list(range(1, 30)),
        "rango_factores": list(range(8, 38)),
    })



