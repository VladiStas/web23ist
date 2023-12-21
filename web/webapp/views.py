from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import *
import requests
import json


# Влад
class UserLogoutView(LogoutView):
    next_page = 'main'


# Данил, Руслан, Влад
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
            if new_user.password == None:
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
        query_result = CompetenceSkillTree.objects.select_related('user').select_related('stack').values('user__login',
                                                                                                         'stack__name',
                                                                                                         'level_of_knowledge')
        loaded_project = Project.objects.select_related('project_admin').values('project_admin__login',
                                                                        'project_name',
                                                                        'status',
                                                                        'about_project',
                                                                        'keywords')
        publications = CompetenceScientificPublications.objects.select_related('authors').values('name',
                                                                                                 'year_of_issue',
                                                                                                 'publication_level',
                                                                                                 'journal',
                                                                                                 'authors')

        courses = CompetenceExtracurricularCourses.objects.select_related('user').values('user',
                                                                                         'name',
                                                                                         'organisation',
                                                                                         'certificate_number',)

        return render(request, 'webapp/user.html', {'user': user_my,
                                                    'title': 'Мой профиль',
                                                    'query_result': query_result,
                                                    'loaded_project': loaded_project,
                                                    'loaded_publications': publications,
                                                    'loaded_courses': courses,
                                                    'current_user_id': request.user.id})


#Даниил
@login_required()
def profile_user_settings(request, user_id):
    data = User.objects.get(pk=user_id)
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number_field')
        email = request.POST.get('email_field')
        course = request.POST.get('course_field')
        group = request.POST.get('group_field')
        about_me = request.POST.get('about_me_field')
        university = request.POST.get('university_field')
        year = request.POST.get('year_field')
        faculty = request.POST.get('faculty_field')
        data.phone_number = phone_number
        data.email = email
        data.course = course
        data.group = group
        data.about_me = about_me
        data.university = university
        data.year = year
        data.faculty = faculty

        data.save()
        return redirect('user', user_id=user_id)  # Изменил параметр на user_id
    return render(request, 'webapp/user-settings.html', {'data': data, 'title': 'Настройка профиля'})


@login_required()
def add_skill(request, user_id):
    if request.method == 'POST':
        stack = request.POST.get('stack')
        print(stack)
        level = request.POST.get('level_of_knowledge')
        competence_skill = CompetenceSkillTree(user_id = user_id,stack_id = stack, level_of_knowledge= level)
        competence_skill.save()
        return redirect('user', user_id=user_id)
    stacks = Stacks.objects.all()
    return render(request, 'webapp/add_skill.html', {'stacks': stacks, 'user_id': user_id})


@login_required()
def add_course(request, user_id):
    name = request.POST.get('name')
    organize = request.POST.get('organize')
    dock = request.POST.get('dock')
    if request.method == 'POST':
        competence_skill = CompetenceExtracurricularCourses(user_id=user_id,name = name, organisation = organize, certificate_number = dock)
        competence_skill.save()
        return redirect('user', user_id=user_id)
    return render(request, 'webapp/add_course.html', {'user_id': user_id})


@login_required()
def add_project(request, user_id):
    if request.method == 'POST':
        project = request.POST.get('project_name')
        status = request.POST.get('status')
        about = request.POST.get('about_project')
        keywords = request.POST.get('keywords')
        projecting = Project(project_admin_id= user_id, project_name= project, status= status, about_project= about, keywords=keywords)
        projecting.save()
        return redirect('user', user_id=user_id)
    projects = Project.objects.all()
    return render(request, 'webapp/add_project.html', {'projects': projects, 'user_id': user_id})


# Андрей
@login_required()
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
    keywords = data.keywords.split(',')
    return render(request, 'webapp/concrete-project.html', {'data': data,
                                                            'keyword': keywords,

                                                            'title': 'Страница проекта'})


@login_required()
@csrf_exempt
def project_settings(request, project_id_settings):
    data = Project.objects.get(pk=project_id_settings)
    if request.method == 'POST':
        project_name = request.POST.get('project_name_field')
        keywords = request.POST.get('keywords_field')
        status = request.POST.get('status_field')
        about_project = request.POST.get('about_field')
        data.project_name = project_name
        data.keywords = keywords
        data.status = status
        data.about_project = about_project
        data.save()

        return redirect('project', project_id=project_id_settings)

    return render(request, 'webapp/project-settings.html', {'data': data,
                                                            'title': 'Настройки проекта'})


# Влад
def pageNotFound(request, exception):
    return HttpResponseNotFound("Страница не найдена :/")

# Андрей
def search_view(request):
    class MyJSONEncoder(json.JSONEncoder):
                def default(self, obj):
                    d = {}
                    d['__class__'] = obj.__class__.__name__
                    d['__module__'] = obj.__module__
                    d.update(obj.__dict__)
                    return d
    query = request.GET.get('query')
    if query:
        if(len(query)>1):
            if(query[0]=="\"" and query[-1]=="\""):
                query=query[1:-1]
            if(len(query)>1):
                if(query[-1]==" "):
                    query=query[:-1]
    DBName = request.GET.get('DBName')
    show_dropdownProjects = False
    show_dropdownStudents = False
    llo=[]

    selectedCategoryProjects = request.GET.get('selectedCategoryProjects')
    selectedTechnologyProjects = request.GET.get('selectedTechnologyProjects')

    selectedCategory = request.GET.get('selectedCategory')
    selectedCourse = request.GET.get('selectedCourse')
    selectedTechnology = request.GET.get('selectedTechnology')
    print(selectedCategoryProjects,selectedTechnologyProjects)
    print(selectedCategory,selectedCourse,selectedTechnology)
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
            dataAnProjects = dataProject
        if(selectedTechnologyProjects!=None):
            dataAnProjectsSort=[]
            for item in dataAnProjects:
                keys_to_remove = list(item.keys())[-2]  # Получаем последний ключ в словаре
                item.pop(keys_to_remove)  # Удаляем последний ключ-значение из словаря
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
            if hasattr(request.user, 'password'):
                del data['user']
            print(dataAnProjects)
            return JsonResponse(data)
        else:
            #print("_______________________________________")
            #print(dataAnProjects)
            #print("---------------------------------")
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
        dataStudents  = UserData.objects.all()
        #print("---------------------------------")
        #print(query)
        #print("---------------------------------")
        dataAnStudents = []
        show_dropdownStudents=True
        if query:
            for students in dataStudents:
                plum=0
                #print("---------------------------------")
                for key, value in students.__dict__.items():
                    #print(str(key).lower(), " : ", str(value).lower())
                    if query.lower() in str(value).lower() and plum == 0:
                        show_dropdownStudents = True
                        dataAnStudents.append(students)
                        plum = 1
        else:
            for students in dataStudents:
                plum=0
                for key, value in students.__dict__.items():
                    if plum == 0:
                        show_dropdownStudents = True
                        dataAnStudents.append(students)
                        plum = 1
        #selectedCategory
        #selectedCourse
        #selectedTechnology
        if(selectedCategory!=None):
            dataAnProjects=dataAnStudents
            dataAnProjectsSort=[]
            if selectedCategory=="allProjects" and selectedCourse=="allProjects" and selectedTechnology=="allProjects" :
                data = {
                'query': query,
                'DBName': DBName,
                'show_dropdownProjects': show_dropdownProjects,
                'show_dropdownStudents': show_dropdownStudents,
                'dataAnProjects': llo,
                'dataAnStudents': dataAnProjects,
                'dataAnExtracurricular': llo,
                'dataAnPublications': llo
                }
            else:
                abcOf1=[]
                abcOf2=[]
                abcOf3=[]
                for students in dataAnProjects:
                    plum=0
                    for key, value in students.__dict__.items():
                        if plum == 0 and (selectedCategory.lower() in str(value).lower() or selectedCategory=="allProjects") and str(key).lower() == "group":
                            abcOf1.append(students)
                            plum = 1
                for students in dataAnProjects:
                    plum=0
                    for key, value in students.__dict__.items():
                        if plum == 0 and (selectedCourse.lower() in str(value).lower() or selectedCourse=="allProjects") and str(key).lower() == "course":
                            abcOf2.append(students)
                            plum = 1
                for students in dataAnProjects:
                    plum=0
                    for key, value in students.__dict__.items():
                        if plum == 0 and (selectedTechnology.lower() in str(value).lower() or selectedTechnology=="allProjects"):
                            abcOf3.append(students)
                            plum = 1
                for student in dataAnProjects:
                    if student in abcOf1 and student in abcOf2 and student in abcOf3:
                        dataAnProjectsSort.append(student)
                #dataAnProjectsSort
                data = {
                'query': query,
                'DBName': DBName,
                'show_dropdownProjects': show_dropdownProjects,
                'show_dropdownStudents': show_dropdownStudents,
                'dataAnProjects': llo,
                'dataAnStudents': dataAnProjectsSort,
                'dataAnExtracurricular': llo,
                'dataAnPublications': llo
                }
            return JsonResponse(data, encoder=MyJSONEncoder)
            #return JsonResponse(data)
        else:
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
