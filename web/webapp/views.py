from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from .models import *
from .forms import UserLoginForm


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'webapp/login.html'
    next_page = 'projects'
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context

    def get_success_url(self):
        return reverse_lazy('projects')


class UserLogoutView(LogoutView):
    next_page = 'projects'


def main(request):
    return render(request, 'webapp/main.html', {'title': 'Главная'})


def user(request):
    return render(request, 'webapp/user.html', {'title': 'Мой профиль'})


def profile_user_settings(request):
    return render(request, 'webapp/user-settings.html', {'title': 'Настройка профиля'})


@login_required()
def projects_template(request):
    data = Project.objects.all()
    return render(request, 'webapp/projects.html', {'data': data, 'title': 'Страница проектов'})


@login_required()
def concrete_project(request, project_id):
    data = Project.objects.all()
    return HttpResponse(f"{project_id}")
    #return render(request, 'webapp/projects.html', {'data': data, 'title': 'Страница проекта'})

#
# @login_required()
# def profile_user(request, id):
#     users = user.objects.get(id=id)
#     return render(request, f'webapp/profile_user/{id}.html', {"users": users})
#     # return redirect(reverse('webapp/profile_user/{id}.html', f'webapp/profile_user/{id}.html', {"users":users}))
