from django.contrib import admin
from .models import Pregunta, Respuesta, IntentoExamen, ConfiguracionExamen

# Register your models here.
admin.site.register(Pregunta)
admin.site.register(Respuesta)
admin.site.register(IntentoExamen)
admin.site.register(ConfiguracionExamen)