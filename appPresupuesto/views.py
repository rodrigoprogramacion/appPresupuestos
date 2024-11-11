from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse
from .models import Trabajo, Categoria
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
from django.conf import settings
import os
from django.contrib.auth.models import User
from .forms import RegistroForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

@login_required
def generar_presupuesto(request):
    if request.method == 'POST':
        cliente = request.POST.get('cliente')
        direccion = request.POST.get('direccion')
        trabajos_seleccionados = request.POST.get('trabajos_input').split(",")  # Recibimos trabajos como lista de IDs

        # Crear el objeto HttpResponse con PDF como tipo de contenido
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="presupuesto.pdf"'

        # Crear un objeto BytesIO para guardar el PDF en memoria
        buffer = BytesIO()

        # Crear un objeto canvas de ReportLab con tamaño A4
        p = canvas.Canvas(buffer, pagesize=A4)
        ancho_pagina, alto_pagina = A4

        # Ruta del logo empresarial
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.png')

        # Encabezado
        if os.path.exists(logo_path):
            p.drawImage(logo_path, 40, alto_pagina - 80, width=120, height=30)
        else:
            p.drawString(40, alto_pagina - 80, "Logo no disponible")

        p.setFont("Helvetica-Bold", 16)
        p.drawString(230, alto_pagina - 80, "Presupuesto de obra")

        # Datos del cliente
        p.setFont("Helvetica", 12)
        p.drawString(40, alto_pagina - 150, f"Cliente: {cliente}")
        p.drawString(40, alto_pagina - 170, f"Dirección: {direccion}")

        # Título de trabajos
        p.setFont("Helvetica-Bold", 12)
        p.drawString(40, alto_pagina - 200, "Trabajos a realizar:")

        # Crear una tabla para los trabajos seleccionados
        y = alto_pagina - 230
        p.setFont("Helvetica", 12)
        total = 0

        # Encabezado de la tabla
        p.setFillColor(colors.grey)
        p.rect(40, y, 500, 20, fill=True, stroke=False)
        p.setFillColor(colors.white)
        p.drawString(50, y + 5, "Descripción")
        p.drawString(400, y + 5, "Precio")
        p.setFillColor(colors.black)

        y -= 30  # Ajustar la posición vertical para los trabajos

        for trabajo_id in trabajos_seleccionados:
            if trabajo_id:
                trabajo = Trabajo.objects.get(id=trabajo_id)
                descripcion = trabajo.descripcion
                precio = trabajo.precio
                total += precio

                p.drawString(50, y, descripcion)  # Descripción del trabajo
                p.drawString(400, y, f"${precio:.2f}")  # Precio del trabajo
                y -= 20  # Espaciado entre filas

        # Dibujar línea final antes del total
        y -= 10
        p.line(40, y, 540, y)
        y -= 30

        # Mostrar el total
        p.setFont("Helvetica-Bold", 12)
        p.drawString(400, y, f"Total: ${total:.2f}")

        # Footer opcional
        p.setFont("Helvetica-Oblique", 10)
        p.drawString(40, 50, "Gracias por confiar en nosotros. Para más información, contáctenos.")

        # Finalizar el PDF
        p.showPage()
        p.save()

        # Obtener el valor del buffer y escribirlo en la respuesta
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    # Si no es POST, mostramos el formulario
    else:
        # Agrupar los trabajos por categoría
        categorias = Categoria.objects.all()
        trabajos_por_categoria = {}
        for categoria in categorias:
            trabajos = Trabajo.objects.filter(categoria=categoria)
            trabajos_por_categoria[categoria.nombre] = trabajos

        return render(request, 'presupuestos/generar_presupuesto.html', {
            'trabajos_por_categoria': trabajos_por_categoria
        })

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Mostrar mensaje de éxito
            messages.success(request, '¡Felicidades! Te has registrado correctamente.')
            return redirect('registro')  # Redirigir al login después del registro exitoso
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirigir al usuario a la página principal después del login
                return redirect('generar_presupuesto')  # O el nombre de la vista a la que quieras redirigir
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

# Vista para cerrar sesión
def cerrar_sesion(request):
    logout(request)
    return redirect('login')
