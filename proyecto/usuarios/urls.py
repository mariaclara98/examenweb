from django.urls import path
from .views import home
from . import views


urlpatterns = [
    path('', home, name='home'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('login/', views.login_usuario, name='login'),
    path('', home, name='home'),
]