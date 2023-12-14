from django.urls import path
from . import views

from .views import UserLoginView, UserLogoutView

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('user/<int:user_id>/', views.user, name='user'),
    path('settings/', views.profile_user_settings, name='settings'),
    path('projects/', views.projects_template, name='projects'),
    path('concrete_project/<int:project_id>/', views.concrete_project, name='project'),
    path('main/', views.main, name='main'),
]
