from django.shortcuts import render, redirect
from usuarios.forms import RegisterForm, InicioSesionForm
from django.contrib import messages
from usuarios.models import Usuario
import yfinance as yf
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login

def portada(request):
    return render(request, "index.html")

def registro(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
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
                # Guardar el usuario en la sesión
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.nombre
                request.session['usuario_documento'] = usuario.documento_identidad
                request.session.modified = True  # Forzar que se guarde la sesión
                messages.success(request, f"Bienvenido {usuario.nombre}")
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
    return render(request, 'interfazAdministrador.html')

def panel(request):
    return render(request, 'panelCalificacion.html')

def panelAdmin(request):
    return render(request, 'panelCalificacionAdmin.html')


