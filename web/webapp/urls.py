from django.urls import path
from . import views

from .views import UserLoginView, UserLogoutView

urlpatterns = [
    # path('index/', views.index, name='index'),
    path('', views.home_visit, name='home_visit'),
    path('profile/', views.profile, name='profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
