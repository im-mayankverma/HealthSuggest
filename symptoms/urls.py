from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('suggestions/', views.get_suggestions, name='get_suggestions'),
]