from django.urls import path
from . import views

urlpatterns = [
    path('SeguroVidaTemporal/', views.CotizadorTemp)
]