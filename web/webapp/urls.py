from django.urls import path
from . import views

from .views import UserLoginView, UserLogoutView

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('user/<int:user_id>/', views.user, name='user'),
    path('settings/<int:user_id>/', views.profile_user_settings, name='settings'),
    path('add_skill/<int:user_id>/', views.add_skill, name='add_skill'),
    path('projects/', views.projects_template, name='projects'),
    path('concrete_project/<int:project_id>/', views.concrete_project, name='project'),
    path('project_settings/<int:project_id_settings>/', views.project_settings, name='project_settings'),
    path('main/', views.main, name='main'),
    path('search_view/', views.search_view, name='search_view'),
]
