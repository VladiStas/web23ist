from django.urls import path, re_path
from . import views
from django.views.generic import RedirectView

from .views import UserLoginView, UserLogoutView

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('user/', views.user, name='user'),
    path('settings/', views.profile_user_settings, name='settings'),
    path('projects/', views.projects_template, name='projects'),
    path('concrete_project/<int:project_id>/', views.concrete_project, name='project'),
    path('main/', views.main, name='main'),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
]
