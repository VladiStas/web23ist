from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from .models import User, Project,Students,CompetenceExtracurricularCourses
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


def search(request):
    return render(request, 'webapp/search.html', {'title': 'Поиск'})


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

def get_data_from_db(request):


    selectedCategoryProjects = request.GET.get('selectedCategoryProjects')
    selectedTechnologyProjects = request.GET.get('selectedTechnologyProjects')
    selectedCategory = request.GET.get('selectedCategory')
    selectedCourse = request.GET.get('selectedCourse')
    selectedTechnology = request.GET.get('selectedTechnology')

    dataProject = Project.get_data_from_db()
    dataStudents  = Students.get_data_from_db()
    dataExtracurricular = CompetenceExtracurricularCourses.get_data_from_db()

    dataAnProjects = []
    if selectedCategoryProjects:

        print(selectedCategoryProjects)
        print(selectedTechnologyProjects)
        print(selectedCategory)
        print(selectedCourse)
        print(selectedTechnology)
        for item in dataProject:
            if item['category'] == selectedCategoryProjects and item['technology'] == selectedTechnologyProjects:
                dataAnProjects.append(item)
    elif selectedCategory:

        print(selectedCategory)
        print(selectedCourse)
        print(selectedTechnology)

    return JsonResponse(dataAnProjects, safe=False)
    #return JsonResponse(dataExtracurricular, safe=False)

def search_view(request):
    dataProject = Project.get_data_from_db()
    dataStudents  = Students.get_data_from_db()
    dataExtracurricular = CompetenceExtracurricularCourses.get_data_from_db()
    query = request.GET.get('query')
    show_dropdownStudents = False  # по умолчанию показываем выпадающий список
    show_dropdownProjects = False
    dataAnProjects = []  # создаем пустой список для хранения данных
    dataAnStudents = []  # создаем пустой список для хранения данных
    dataAnExtracurricular = []  # создаем пустой список для хранения данных
    selectedCategoryProjects = request.GET.get('selectedCategoryProjects')
    selectedTechnologyProjects = request.GET.get('selectedTechnologyProjects')
    selectedCategory = request.GET.get('selectedCategory')
    selectedCourse = request.GET.get('selectedCourse')
    selectedTechnology = request.GET.get('selectedTechnology')
    selectedCategoryProjects2=""
    selectedTechnologyProjects2=""
    if selectedCategoryProjects:
        if(selectedCategoryProjects == "categoryProjects1"):
            selectedCategoryProjects="ищет команд"
        elif(selectedCategoryProjects == "categoryProjects2"):
            selectedCategoryProjects="в процесс"
        elif(selectedCategoryProjects == "categoryProjects3"):
            selectedCategoryProjects="В разработ"
        elif(selectedCategoryProjects == "categoryProjects4"):
            selectedCategoryProjects="близок к заверш"
        elif(selectedCategoryProjects == "categoryProjects5"):
            selectedCategoryProjects="прототипировани"
        elif(selectedCategoryProjects == "categoryProjects6"):
            selectedCategoryProjects="завершён"
        elif(selectedCategoryProjects == "categoryProjects7"):
            selectedCategoryProjects="Отменё"
        elif(selectedCategoryProjects == "allProjects"):
            selectedCategoryProjects=""
            selectedCategoryProjects2="allProjects"

        if(selectedTechnologyProjects == "techProjects1"):
            selectedTechnologyProjects="c++"
        elif(selectedTechnologyProjects == "techProjects2"):
            selectedTechnologyProjects="python"
        elif(selectedTechnologyProjects == "techProjects3"):
            selectedTechnologyProjects="java script"
        elif(selectedTechnologyProjects == "techProjects4"):
            selectedTechnologyProjects="c#"
        elif(selectedTechnologyProjects == "allProjects"):
            selectedTechnologyProjects=""
            selectedTechnologyProjects2= "allProjects"
        print(selectedCategoryProjects)
        print(selectedTechnologyProjects)

    elif selectedCategory:

        print(selectedCategory)
        print(selectedCourse)
        print(selectedTechnology)

    if query:
        for project in dataProject:
            plum=0
            for value in project.values():
                if query.lower() in str(value).lower() and plum==0:
                    show_dropdownProjects = True    # скрываем выпадающий список
                    dataAnProjects.append(project)  # добавляем данные в dataAnProjects
                    plum=1
        for students in dataStudents:
            plum=0
            for value in students.values():
                if query.lower() in str(value).lower() and plum==0:
                    show_dropdownStudents = True
                    dataAnStudents.append(students)
                    plum=1
        for extracurricular in dataExtracurricular:
            plum=0
            for value in extracurricular.values():
                if query.lower() in str(value).lower() and plum==0:
                    dataAnExtracurricular.append(extracurricular)
                    plum=1
    '''elif query and query == "Stud":
        show_dropdownProjects = False
        show_dropdownStudents = True'''
    if query and query == "":
        show_dropdownStudents = False
        show_dropdownProjects = False
    dataAnProjects2=[]
    for value in dataAnProjects:
        #print(value)
        if selectedCategoryProjects:
            if selectedCategoryProjects.lower() in str(value).lower() and selectedTechnologyProjects.lower() in str(value).lower():
                show_dropdownProjects = True    # скрываем выпадающий список
                dataAnProjects2.append(value)  # добавляем данные в dataAnProjects2
    for value in dataAnProjects:
        #print(value)
        if selectedTechnologyProjects:
            if selectedTechnologyProjects.lower() in str(value).lower() and selectedTechnologyProjects!="":
                show_dropdownProjects = True    # скрываем выпадающий список
                dataAnProjects2.append(value)  # добавляем данные в dataAnProjects2
    if selectedCategoryProjects!=None:
        print("-----------------------------------------")
        print(dataAnProjects2)
        print(dataAnProjects)
        print("_________________________________________________________________________")
        if selectedCategoryProjects2=="allProjects" and selectedTechnologyProjects2=="allProjects":
            data = {
            'query': query,
            'show_dropdownProjects': show_dropdownProjects,
            'show_dropdownStudents': show_dropdownStudents,
            'dataAnProjects': dataAnProjects,
            'dataAnStudents': dataAnStudents,
            'dataAnExtracurricular': dataAnExtracurricular
            }

        else:
            data = {
            'query': query,
            'show_dropdownProjects': show_dropdownProjects,
            'show_dropdownStudents': show_dropdownStudents,
            'dataAnProjects': dataAnProjects2,
            'dataAnStudents': dataAnStudents,
            'dataAnExtracurricular': dataAnExtracurricular
            }


        return JsonResponse(data)
    else:
        return render(request, 'webapp/search.html', {'query': query, 'show_dropdownProjects': show_dropdownProjects, 'show_dropdownStudents': show_dropdownStudents, 'dataAnProjects': dataAnProjects, 'dataAnStudents': dataAnStudents, 'dataAnExtracurricular': dataAnExtracurricular})

