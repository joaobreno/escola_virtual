from django.contrib import admin
from .models import *

# Register your models here.

class EstudanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')

admin.site.register(Estudante, EstudanteAdmin)