from django.urls import path
from . import views

urlpatterns = [
    path('solicitud/', views.solicitar_credito, name='solicitar_credito'),
    
]