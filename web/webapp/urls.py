from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.authorization, name='authorization'),
    path('profile/', views.profile, name='profile'),
]
