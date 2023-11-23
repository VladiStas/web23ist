from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserLoginForm


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'webapp/authorization.html'
    next_page = 'profile'
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context


class UserLogoutView(LogoutView):
    next_page = 'home_visit'


def index(request):
    context = {
        'products': ['Яблоко', 'Банан', 'Апельсин'],
    }
    return render(request, 'webapp/index.html', context)


@login_required()
def profile(request):
    return render(request, 'webapp/profile.html')


def home_visit(request):
    return render(request, 'webapp/home_visit.html')


def authorization(request):
    if request.method == 'POST':
        return redirect('profile')
    else:
        return render(request, 'webapp/authorization.html')
