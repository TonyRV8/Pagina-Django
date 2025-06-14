from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Usuario
from .forms import LoginForm, RegisterForm
from django.db import transaction
import traceback

def index(request):
    """Vista principal"""
    return render(request, 'index.html')

def login_view(request):
    """Vista para el login con debug"""
    print("🔍 DEBUG LOGIN: Entrando a login_view")
    print(f"🔍 DEBUG LOGIN: Método: {request.method}")
    
    if request.method == 'POST':
        print("🔍 DEBUG LOGIN: Procesando POST")
        form = LoginForm(request.POST)
        print(f"🔍 DEBUG LOGIN: Form data: {request.POST}")
        
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            contrasena = form.cleaned_data['contrasena']
            print(f"🔍 DEBUG LOGIN: Intentando login con usuario: '{usuario}' y contraseña: '{contrasena}'")
            
            try:
                # Buscar usuario
                user = Usuario.objects.get(usuario=usuario, contrasena=contrasena, activo=True)
                request.session['usuario_id'] = user.id
                request.session['usuario_nombre'] = user.usuario
                messages.success(request, f'¡Bienvenido, {user.usuario}!')
                print(f"🔍 DEBUG LOGIN: Login exitoso para: {usuario}")
                return redirect('dashboard')
            except Usuario.DoesNotExist:
                print(f"🔍 DEBUG LOGIN: Usuario no encontrado o contraseña incorrecta")
                print(f"🔍 DEBUG LOGIN: Usuarios disponibles en BD:")
                for u in Usuario.objects.all():
                    print(f"  - Usuario: '{u.usuario}', Contraseña: '{u.contrasena}', Activo: {u.activo}")
                messages.error(request, 'Usuario o contraseña incorrectos.')
            except Exception as e:
                print(f"🔍 DEBUG LOGIN: Error inesperado: {e}")
                messages.error(request, f'Error en el sistema: {e}')
        else:
            print(f"🔍 DEBUG LOGIN: Errores en formulario: {form.errors}")
            messages.error(request, f'Errores en formulario: {form.errors}')
    else:
        print("🔍 DEBUG LOGIN: Creando formulario GET")
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def register_view(request):
    """Vista para el registro con debug detallado"""
    print("🔍 DEBUG REGISTER: Entrando a register_view")
    print(f"🔍 DEBUG REGISTER: Método: {request.method}")
    
    if request.method == 'POST':
        print("🔍 DEBUG REGISTER: Procesando POST")
        print(f"🔍 DEBUG REGISTER: Form data: {request.POST}")
        
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            usuario_data = {
                'usuario': form.cleaned_data['usuario'],
                'contrasena': form.cleaned_data['contrasena'],
                'correo': form.cleaned_data['correo']
            }
            print(f"🔍 DEBUG REGISTER: Datos validados: {usuario_data}")
            
            try:
                with transaction.atomic():
                    # Verificar que no exista el usuario
                    if Usuario.objects.filter(usuario=usuario_data['usuario']).exists():
                        print(f"🔍 DEBUG REGISTER: Usuario '{usuario_data['usuario']}' ya existe")
                        messages.error(request, 'El usuario ya existe.')
                        return render(request, 'register.html', {'form': form})
                    
                    if Usuario.objects.filter(correo=usuario_data['correo']).exists():
                        print(f"🔍 DEBUG REGISTER: Email '{usuario_data['correo']}' ya existe")
                        messages.error(request, 'El correo ya está registrado.')
                        return render(request, 'register.html', {'form': form})
                    
                    # Crear usuario
                    print(f"🔍 DEBUG REGISTER: Creando usuario en BD...")
                    nuevo_usuario = Usuario.objects.create(
                        usuario=usuario_data['usuario'],
                        contrasena=usuario_data['contrasena'],
                        correo=usuario_data['correo'],
                        activo=True
                    )
                    print(f"🔍 DEBUG REGISTER: Usuario creado con ID: {nuevo_usuario.id}")
                    
                    # Verificar que se guardó
                    usuario_verificacion = Usuario.objects.get(id=nuevo_usuario.id)
                    print(f"🔍 DEBUG REGISTER: Verificación - Usuario guardado: {usuario_verificacion.usuario}")
                    
                    messages.success(request, '¡Cuenta creada exitosamente! Ya puedes iniciar sesión.')
                    print(f"🔍 DEBUG REGISTER: Usuario '{usuario_data['usuario']}' creado exitosamente")
                    
                    return redirect('login')
                    
            except Exception as e:
                print(f"🔍 DEBUG REGISTER: Error al crear usuario: {e}")
                print(f"🔍 DEBUG REGISTER: Traceback: {traceback.format_exc()}")
                messages.error(request, f'Error al crear la cuenta: {e}')
        else:
            print(f"🔍 DEBUG REGISTER: Errores en formulario:")
            for field, errors in form.errors.items():
                print(f"  - {field}: {errors}")
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        print("🔍 DEBUG REGISTER: Creando formulario GET")
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

def dashboard_view(request):
    """Vista del dashboard"""
    print("🔍 DEBUG DASHBOARD: Entrando a dashboard_view")
    usuario_id = request.session.get('usuario_id')
    print(f"🔍 DEBUG DASHBOARD: Usuario ID en sesión: {usuario_id}")
    
    if not usuario_id:
        messages.error(request, 'Debes iniciar sesión para acceder.')
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        print(f"🔍 DEBUG DASHBOARD: Usuario encontrado: {usuario.usuario}")
    except Usuario.DoesNotExist:
        print("🔍 DEBUG DASHBOARD: Usuario no encontrado, limpiando sesión")
        del request.session['usuario_id']
        messages.error(request, 'Sesión inválida.')
        return redirect('login')
    
    return render(request, 'dashboard.html', {'usuario': usuario})

def profile_view(request):
    """Vista del perfil"""
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        del request.session['usuario_id']
        return redirect('login')
    
    return render(request, 'profile.html', {'usuario': usuario})

def logout_view(request):
    """Vista para cerrar sesión"""
    usuario_nombre = request.session.get('usuario_nombre', 'Usuario')
    request.session.flush()
    messages.info(request, f'¡Hasta luego, {usuario_nombre}! Has cerrado sesión.')
    return redirect('index')