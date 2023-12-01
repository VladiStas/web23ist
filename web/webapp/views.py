from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from .models import user
from .forms import UserLoginForm


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'webapp/authorization.html'
    next_page = 'profile_user'
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context


class UserLogoutView(LogoutView):
    next_page = 'home_visit'


def home_visit(request):
    return render(request, 'webapp/home_visit.html')


def home_settings(request):
    return render(request, 'webapp/home_settings.html')


def home_user(request):
    return render(request, 'webapp/home_user.html')


def settings(request):
    return render(request, 'webapp/settings.html')


def home(request):
    return render(request, 'webapp/home.html')


def any_page(request, page_name):
    return render(request, f'webapp/{page_name}.html')


@login_required()
def profile_user(request, id):
    users = user.objects.get(id=id)
    return render(request, f'webapp/profile_user/{id}.html', {"users":users})
    # return redirect(reverse('webapp/profile_user/{id}.html', f'webapp/profile_user/{id}.html', {"users":users}))


def home_project(request):
    users = user.objects.get(id=id)
    return render(request, 'webapp/home_project.html')


def authorization(request):
    if request.method == 'POST':
        return redirect('profile')
    else:
        return render(request, 'webapp/authorization.html')
