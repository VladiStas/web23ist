from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.hashers import make_password
from .models import *
from .forms import UserLoginForm
import requests


# Влад
class UserLogoutView(LogoutView):
    next_page = 'main'


# Данил, Рулсан, Влад
# TODO Поменять верхний класс на нижний в релизе
class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'webapp/login.html'
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context

    def post(self, request, *args, **kwargs):
        # Получение данных из POST-запроса до валидации формы
        username = request.POST.get('username')
        password = request.POST.get('password')

        payload = {
            'username': username,
            'password': password,
        }

        response1 = requests.post('http://localhost:7000/api/Auth/auth', json=payload)

        if response1.status_code == 200:
            new_user = User.objects.get(login=username)
            new_user.password = make_password(password)
            new_user.save()

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        print("Login successful!")
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        print("Login failed!")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('main')


# Влад
def main(request):
    return render(request, 'webapp/main.html', {'title': 'Главная'})


@login_required()
def user(request, user_id):
        user_my = User.objects.get(pk=user_id)
        return render(request, 'webapp/user.html', {'user': user_my,
                                                    'title': 'Мой профиль',
                                                    'current_user_id': request.user.id})


def profile_user_settings(request):
    return render(request, 'webapp/user-settings.html', {'title': 'Настройка профиля'})


# Андрей
def search(request):
    return render(request, 'webapp/search.html', {'title': 'Поиск'})


# Влад, Илья
@login_required()
def projects_template(request):
    data = Project.objects.all()
    return render(request, 'webapp/projects.html', {'data': data, 'title': 'Страница проектов'})


# Илья
@login_required()
def concrete_project(request, project_id):
    data = Project.objects.get(pk=project_id)
    user_my = User.objects.all()
    keywords = data.keywords.split(',')
    return render(request, 'webapp/concrete-project.html', {'data': data,
                                                            'keyword': keywords,
                                                            'user': user_my,
                                                            'title': 'Страница проекта'})


# Влад
def pageNotFound(request, exception):
    return HttpResponseNotFound("Страница не найдена :/")

# Андрей
def search_view(request):
    query = request.GET.get('query')
    query=query[1:-1]
    DBName = request.GET.get('DBName')
    show_dropdownProjects = False
    show_dropdownStudents = False
    llo=[]

    selectedCategoryProjects = request.GET.get('selectedCategoryProjects')
    selectedTechnologyProjects = request.GET.get('selectedTechnologyProjects')

    selectedCategory = request.GET.get('selectedCategory')
    selectedCourse = request.GET.get('selectedCourse')
    selectedTechnology = request.GET.get('selectedTechnology')

    if(DBName=="projects"):
        dataProject = Project.get_data_from_db() # хранилище данных из БД
        dataAnProjects = []  # создаем пустой список для хранения данных projects
        show_dropdownProjects=True # включаем сортировку для данных

        if query:
            for project in dataProject:
                plum=0
                for value in project.values():
                    if query.lower() in str(value).lower() and plum==0:
                        dataAnProjects.append(project)  # добавляем данные в dataAnProjects
                        plum=1
        else:
            print(DBName)
            dataAnProjects = dataProject
        if(selectedTechnologyProjects!=None):
            dataAnProjectsSort=[]
            if selectedCategoryProjects != "allProjects":
                for value in dataAnProjects:
                    if selectedCategoryProjects.lower() in str(value).lower() and (selectedTechnologyProjects.lower() in str(value).lower() or selectedTechnologyProjects=="allProjects"):
                        dataAnProjectsSort.append(value)
            if selectedTechnologyProjects!= "allProjects":
                for value in dataAnProjects:
                    if selectedTechnologyProjects.lower() in str(value).lower() and selectedTechnologyProjects!="":
                        dataAnProjectsSort.append(value)
            if selectedCategoryProjects=="allProjects" and selectedTechnologyProjects=="allProjects":
                data = {
                'query': query,
                'DBName': DBName,
                'show_dropdownProjects': show_dropdownProjects,
                'show_dropdownStudents': show_dropdownStudents,
                'dataAnProjects': dataAnProjects,
                'dataAnStudents': llo,
                'dataAnExtracurricular': llo,
                'dataAnPublications': llo
                }
            else:
                data = {
                'query': query,
                'DBName': DBName,
                'show_dropdownProjects': show_dropdownProjects,
                'show_dropdownStudents': show_dropdownStudents,
                'dataAnProjects': dataAnProjectsSort,
                'dataAnStudents': llo,
                'dataAnExtracurricular': llo,
                'dataAnPublications': llo
                }
            return JsonResponse(data)
        else:
            print("_______________________________________")
            print(dataAnProjects)
            print("---------------------------------")
            print("---+---+---+---+---+---+---")
            return render(request, 'webapp/search.html', {'query': query, 'DBName': DBName, 'show_dropdownProjects': show_dropdownProjects, 'show_dropdownStudents': show_dropdownStudents, 'dataAnProjects': dataAnProjects, 'dataAnStudents': llo, 'dataAnExtracurricular': llo, 'dataAnPublications': llo})
    elif(DBName=="competence_extracurricular_courses"):
        dataExtracurricular = CompetenceExtracurricularCourses.get_data_from_db()
        dataAnExtracurricular = []
        if query:
            for extracurricular in dataExtracurricular:
                plum=0
                for value in extracurricular.values():
                    if query.lower() in str(value).lower() and plum==0:
                        dataAnExtracurricular.append(extracurricular)
                        plum=1
        else:
            dataAnExtracurricular=dataExtracurricular
        return render(request, 'webapp/search.html', {'query': query, 'DBName': DBName, 'show_dropdownProjects': show_dropdownProjects, 'show_dropdownStudents': show_dropdownStudents, 'dataAnProjects': llo, 'dataAnStudents': llo, 'dataAnExtracurricular': dataAnExtracurricular, 'dataAnPublications': llo})
    elif(DBName=="students"):
        dataStudents  = UserData.get_data_from_db()
        dataAnStudents = []
        show_dropdownStudents=True
        if query:
            for students in dataStudents:
                plum=0
                for value in students.values():
                    if query.lower() in str(value).lower() and plum==0:
                        show_dropdownStudents = True
                        dataAnStudents.append(students)
                        plum=1
        else:
            dataAnStudents=dataStudents
        return render(request, 'webapp/search.html', {'query': query, 'DBName': DBName, 'show_dropdownProjects': show_dropdownProjects, 'show_dropdownStudents': show_dropdownStudents, 'dataAnProjects': llo, 'dataAnStudents': dataAnStudents, 'dataAnExtracurricular': llo, 'dataAnPublications': llo})
    elif(DBName=="competence_scientific_publications"):
        dataPublications = CompetenceScientificPublications.get_data_from_db()
        dataAnPublications = []
        if query:
            for publications in dataPublications:
                plum=0
                for value in publications.values():
                    if query.lower() in str(value).lower() and plum==0:
                        dataAnPublications.append(publications)
                        plum=1
        else:
            dataAnPublications=dataPublications
        return render(request, 'webapp/search.html', {'query': query, 'DBName': DBName, 'show_dropdownProjects': show_dropdownProjects, 'show_dropdownStudents': show_dropdownStudents, 'dataAnProjects': llo, 'dataAnStudents': llo, 'dataAnExtracurricular': llo, 'dataAnPublications': dataAnPublications})


    return render(request, 'webapp/search.html', {'query': query, 'DBName': DBName, 'show_dropdownProjects': show_dropdownProjects, 'show_dropdownStudents': show_dropdownStudents, 'dataAnProjects': llo, 'dataAnStudents': llo, 'dataAnExtracurricular': llo, 'dataAnPublications': llo})

