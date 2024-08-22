from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pregunta(models.Model):
    enunciado = models.TextField()
    def __str__(self):
        return f"{self.id}, {self.enunciado}" 

class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto = models.TextField()
    es_correcta = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.pregunta.enunciado}, {self.texto}, {self.es_correcta}" 

class ConfiguracionExamen(models.Model):
    tiempo_limite = models.IntegerField(help_text="Tiempo en minutos", default=10)
    calificacion_maxima = models.IntegerField(default=20)
    numero_preguntas = models.IntegerField(default=10)

    def tiempo_limite_segundos(self):
        return self.tiempo_limite * 60


class IntentoExamen(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    calificacion = models.FloatField()
    numero_aciertos = models.IntegerField()
    numero_fallos = models.IntegerField()

    def __str__(self):
        return f"Intento de {self.usuario.username} - {self.fecha_hora} - Nota: {self.calificacion}"


