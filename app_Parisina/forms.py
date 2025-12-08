from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    direccion = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    correo = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    codigo_postal = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'telefono', 'direccion', 'correo', 'codigo_postal']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre de Usuario'
        self.fields['email'].label = 'Correo Electrónico (para la cuenta)'
        self.fields['correo'].label = 'Correo Electrónico (de contacto)'
        self.fields['telefono'].label = 'Teléfono'
        self.fields['direccion'].label = 'Dirección'
        self.fields['codigo_postal'].label = 'Código Postal'
        
        self.fields['username'].widget.attrs.update({'placeholder': 'Elige un nombre de usuario'})
        self.fields['email'].widget.attrs.update({'placeholder': 'ejemplo@correo.com'})
        self.fields['correo'].widget.attrs.update({'placeholder': 'ejemplo@correo.com'})
        self.fields['telefono'].widget.attrs.update({'placeholder': '55 1234 5678'})
        self.fields['direccion'].widget.attrs.update({'placeholder': 'Calle, número, colonia'})
        self.fields['codigo_postal'].widget.attrs.update({'placeholder': '12345'})

class TelaForm(forms.ModelForm):
    class Meta:
        model = Telas
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_tela': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidad': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

class DecoracionForm(forms.ModelForm):
    class Meta:
        model = Decoracion
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'material': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidad': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

class MerceriaForm(forms.ModelForm):
    class Meta:
        model = MerceriaManualidad
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidad': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

class HogarForm(forms.ModelForm):
    class Meta:
        model = Hogar
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_articulo': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'material': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidad': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la empresa'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }