# Verifica que este archivo existe: app/forms.py
from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=50, label='Usuario')
    contrasena = forms.CharField(widget=forms.PasswordInput(), label='Contraseña')

class RegisterForm(forms.Form):
    usuario = forms.CharField(max_length=50, label='Usuario')
    correo = forms.EmailField(label='Correo')
    contrasena = forms.CharField(widget=forms.PasswordInput(), label='Contraseña')
    confirmar_contrasena = forms.CharField(widget=forms.PasswordInput(), label='Confirmar Contraseña')

    def clean_usuario(self):
        usuario = self.cleaned_data['usuario']
        if Usuario.objects.filter(usuario=usuario).exists():
            raise ValidationError('Este usuario ya existe.')
        return usuario

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if Usuario.objects.filter(correo=correo).exists():
            raise ValidationError('Este correo ya está registrado.')
        return correo

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get('contrasena')
        confirmar_contrasena = cleaned_data.get('confirmar_contrasena')
        if contrasena and confirmar_contrasena and contrasena != confirmar_contrasena:
            raise ValidationError('Las contraseñas no coinciden.')
        return cleaned_data