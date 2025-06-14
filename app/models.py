from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

class Usuario(models.Model):
    usuario = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=255)
    correo = models.EmailField(unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return self.usuario

@receiver(post_migrate)
def crear_usuarios_por_defecto(sender, **kwargs):
    """
    Crear usuarios por defecto después de ejecutar migraciones
    Se ejecuta automáticamente después de 'python manage.py migrate'
    """
    # Solo ejecutar para la app 'app' y evitar problemas con otras apps
    if sender.name == 'app':
        print("🚀 Verificando usuarios por defecto...")
        
        # Obtener el modelo Usuario
        try:
            Usuario = apps.get_model('app', 'Usuario')
        except LookupError:
            print("❌ Modelo Usuario no encontrado, saltando creación de usuarios.")
            return
        
        # Lista de usuarios por defecto
        usuarios_por_defecto = [
            {
                'usuario': 'admin',
                'correo': 'admin@example.com',
                'contrasena': 'admin123',
                'activo': True
            },
            {
                'usuario': 'usuario1',
                'correo': 'usuario1@example.com',
                'contrasena': 'password123',
                'activo': True
            },
            {
                'usuario': 'test',
                'correo': 'test@example.com',
                'contrasena': 'test123',
                'activo': True
            },
            {
                'usuario': 'demo',
                'correo': 'demo@example.com',
                'contrasena': 'demo123',
                'activo': True
            },
            {
                'usuario': 'invitado',
                'correo': 'invitado@example.com',
                'contrasena': 'invitado123',
                'activo': True
            },
            {
                'usuario': 'supervisor',
                'correo': 'supervisor@example.com',
                'contrasena': 'supervisor123',
                'activo': True
            }
        ]
        
        usuarios_creados = 0
        usuarios_existentes = 0
        
        for usuario_data in usuarios_por_defecto:
            # Verificar si el usuario ya existe
            if not Usuario.objects.filter(usuario=usuario_data['usuario']).exists():
                # Verificar si el correo ya existe
                if not Usuario.objects.filter(correo=usuario_data['correo']).exists():
                    try:
                        Usuario.objects.create(**usuario_data)
                        print(f"✅ Usuario creado: {usuario_data['usuario']} ({usuario_data['correo']})")
                        usuarios_creados += 1
                    except Exception as e:
                        print(f"❌ Error creando usuario {usuario_data['usuario']}: {e}")
                else:
                    print(f"⚠️ Email ya existe: {usuario_data['correo']}")
                    usuarios_existentes += 1
            else:
                print(f"⚠️ Usuario ya existe: {usuario_data['usuario']}")
                usuarios_existentes += 1
        
        # Resumen final
        total_usuarios = Usuario.objects.count()
        print(f"\n📊 RESUMEN DE USUARIOS:")
        print(f"   • Usuarios creados en esta ejecución: {usuarios_creados}")
        print(f"   • Usuarios que ya existían: {usuarios_existentes}")
        print(f"   • Total de usuarios en la BD: {total_usuarios}")
        
        if usuarios_creados > 0:
            print(f"\n👥 NUEVOS USUARIOS DISPONIBLES:")
            for usuario_data in usuarios_por_defecto:
                if not Usuario.objects.filter(usuario=usuario_data['usuario']).exists():
                    continue
                print(f"   • {usuario_data['usuario']} / {usuario_data['contrasena']} ({usuario_data['correo']})")
        
        print("🎉 Proceso de creación de usuarios completado!")

# Función auxiliar para obtener la lista de usuarios (opcional)
def obtener_usuarios_demo():
    """Función para obtener lista de credenciales de usuarios demo"""
    return [
        {'usuario': 'admin', 'contrasena': 'admin123', 'tipo': 'Administrador'},
        {'usuario': 'usuario1', 'contrasena': 'password123', 'tipo': 'Usuario normal'},
        {'usuario': 'test', 'contrasena': 'test123', 'tipo': 'Usuario de prueba'},
    ]