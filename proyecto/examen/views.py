from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .models import Pregunta, Respuesta, ConfiguracionExamen, IntentoExamen
import random

@login_required
def examen(request):
    if request.method == 'POST':
        configuracion = ConfiguracionExamen.objects.first()
        if not configuracion:
            return HttpResponseBadRequest("No hay configuración de examen disponible.")
        
        preguntas = list(Pregunta.objects.all())
        if len(preguntas) < configuracion.numero_preguntas:
            return HttpResponseBadRequest("No hay suficientes preguntas en la base de datos.")
        
        preguntas_seleccionadas = random.sample(preguntas, configuracion.numero_preguntas)
        
        # Calcular el puntaje
        puntaje = 0

        for pregunta in preguntas_seleccionadas:
            respuesta_id = request.POST.get(f'respuesta{pregunta.id}')
            print(f"Pregunta ID: {pregunta.id}, Respuesta seleccionada: {respuesta_id}")
            if respuesta_id:
                try:
                    respuesta = Respuesta.objects.get(id=respuesta_id)
                    print(f"Respuesta correcta: {respuesta.es_correcta}")
                    if respuesta.es_correcta:
                        puntaje += 1
                except Respuesta.DoesNotExist:
                    print("Respuesta no encontrada")
        
        # Calcular la calificación
        calificacion_maxima = configuracion.calificacion_maxima
        calificacion = (puntaje / configuracion.numero_preguntas) * calificacion_maxima
        
        # Guardar intento de examen
        intento = IntentoExamen(
            usuario=request.user,
            calificacion=calificacion,
            numero_aciertos=puntaje,
            numero_fallos=(configuracion.numero_preguntas - puntaje)
        )
        intento.save()
        
        return render(request, 'examen/resultado_examen.html', {
            'puntaje': puntaje,
            'total_preguntas': configuracion.numero_preguntas,
            'calificacion': calificacion
        })
    
    else:
        configuracion = ConfiguracionExamen.objects.first()
        if not configuracion:
            return HttpResponseBadRequest("No hay configuración de examen disponible.")
        
        preguntas = list(Pregunta.objects.all())
        if len(preguntas) < configuracion.numero_preguntas:
            return HttpResponseBadRequest("No hay suficientes preguntas en la base de datos.")
        
        preguntas_seleccionadas = random.sample(preguntas, configuracion.numero_preguntas)
        
        tiempo_limite = configuracion.tiempo_limite * 60  # Tiempo en segundos
        
        context = {
            'preguntas': preguntas_seleccionadas,
            'tiempo_limite': tiempo_limite
        }
        
        return render(request, 'examen/examen.html', context)
