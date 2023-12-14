from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from .models import *
from .forms import UserLoginForm


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'webapp/login.html'
    next_page = 'main'
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context

    def get_success_url(self):
        return reverse_lazy('main')


class UserLogoutView(LogoutView):
    next_page = 'main'


# TODO Поменять верхний класс на нижний в релизе
# class UserLoginView(SuccessMessageMixin, LoginView):
#     form_class = UserLoginForm
#     template_name = 'webapp/login.html'
#     success_message = 'Добро пожаловать на сайт!'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Авторизация на сайте'
#         return context
#
#     def form_valid(self, form):
#         print("Login successful!")  # Добавьте эту строку
#         response = super().form_valid(form)
#         # Подготовка данных для POST-запроса
#         payload = {
#             'username': form.cleaned_data['username'],  # Обратите внимание на использование cleaned_data
#             'password': form.cleaned_data['password'],
#             # Другие данные, если необходимо
#         }
#
#         # Ваш запрос. Предполагается, что ваш сервер ожидает POST-запрос.
#         response1 = requests.post('http://localhost:5228/api/Auth/auth', json=payload)
#
#         if response1.status_code == 200:
#             # Если успешно, например, можете сохранить токен в сессии или куках
#             # и затем перенаправить пользователя
#             print(response1.json())
#             return response
#         else:
#             # Если запрос неудачен, вы можете обработать ошибку или принять другие меры
#             print('Authentication failed')
#             return response
#
#     def form_invalid(self, form):
#         print("Login failed!")  # Добавьте эту строку
#         return super().form_invalid(form)
#
#     def get_success_url(self):
#         # После успешной авторизации, перенаправляем пользователя на вкладку проектов
#         return reverse_lazy('user')


def main(request):
    return render(request, 'webapp/main.html', {'title': 'Главная'})


@login_required()
def user(request, user_id):
        user_my = UserData.objects.get(pk=user_id)
        #user_data = user_my.user_data
        return render(request, 'webapp/user.html', {'user': user_my,
                                                    'title': 'Мой профиль',
                                                    # 'user_data': user_data,
                                                    'current_user_id': request.user.id})


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


def pageNotFound(request, exception):
    return HttpResponseNotFound("Страница не найдена :/")
