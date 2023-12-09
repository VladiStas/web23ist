from django.urls import path
from . import views

from .views import UserLoginView, UserLogoutView

urlpatterns = [
    # path('', views.home_visit, name='home_visit'),
    path('', views.main, name='main'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile_user/', views.profile_user, name='profile_user'),
    path('projects/', views.projects_template, name='projects'),
    path('main/', views.main, name='main'),
]
