from django.urls import path
from . import views

from .views import UserLoginView, UserLogoutView

urlpatterns = [
    path('', views.home_visit, name='home_visit'),
    path('profile/', views.profile, name='profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('home_settings/', views.home_settings, name='home_settings'),
    path('home_user/', views.home_user, name='home_user'),
    path('settings/', views.settings, name='settings'),
    path('home/', views.home, name='home'),
    path('profile_user/', views.profile_user, name='profile_user'),
]
