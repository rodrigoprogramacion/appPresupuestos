from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [    
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('generar_presupuesto/', views.generar_presupuesto, name='generar_presupuesto'),  # Presupuesto
]
