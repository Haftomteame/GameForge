from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    path('generate/', views.generate_game, name='generate_game'),
    path('generate/random/', views.generate_random, name='generate_random'),
] 