from django import forms
from .models import Trabajo
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TrabajoForm(forms.Form):
    # Campos para los datos del cliente
    nombre_cliente = forms.CharField(label="Nombre del Cliente", max_length=100)
    direccion_cliente = forms.CharField(label="Dirección del Cliente", max_length=200)
    telefono_cliente = forms.CharField(label="Teléfono del Cliente", max_length=20)
    email_cliente = forms.EmailField(label="Correo Electrónico del Cliente")

    # Selección de trabajos
    trabajos = forms.ModelMultipleChoiceField(
        queryset=Trabajo.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Selecciona los trabajos para el presupuesto"
    )

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
