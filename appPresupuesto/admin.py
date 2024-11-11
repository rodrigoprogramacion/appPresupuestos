from django.contrib import admin
from .models import Categoria, Trabajo

# Registro de modelos para el admin
class TrabajoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'categoria', 'precio')
    list_filter = ('categoria',)
    search_fields = ('descripcion',)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Trabajo, TrabajoAdmin)
