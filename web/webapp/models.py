from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models
from django.urls import reverse
from django import forms


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('hide_contacts', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('hide_contacts', False)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    class Meta:
        managed = False
        db_table = "user"
        verbose_name = "Пользователи"

    last_login = models.DateTimeField()
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    photo = models.BinaryField(null=True, editable=True)
    email = models.CharField(max_length=50)
    telegram_nick = models.CharField(max_length=50)
    university = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    course = models.IntegerField()
    phone_number = models.CharField(max_length=50)
    about_me = models.CharField(max_length=50)
    faculty = models.CharField(max_length=50)
    hide_contacts = models.BooleanField()
    objects = CustomUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    def get_url(self):
        return reverse('user', kwargs={'user_id': self.pk})

    def __str__(self):
        return self.email


class Project(models.Model):
    class Meta:
        db_table = "projects"
        verbose_name = "Проекты"

    project_name = models.CharField(max_length=100)
    status = models.CharField(max_length=15)
    about_project = models.CharField(max_length=600)
    keywords = models.CharField(max_length=128)
    project_admin = models.ForeignKey(User, on_delete=models.CASCADE)

    # FK_projects_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_url(self):
        return reverse('project', kwargs={'project_id': self.pk})

    @staticmethod
    def get_data_from_db():
        projects = Project.objects.all()
        data = [{
            'project_name': project.project_name,
            'status': project.status,
            'about_project': project.about_project,
            'project_admin': project.project_admin,
            'keywords': project.keywords,
        } for project in projects]
        return data


class Stacks(models.Model):
    class Meta:
        db_table = "stacks"
        verbose_name = "Дисциплины"

    name = models.CharField(max_length=50)


class CompetenceSkillTree(models.Model):
    class Meta:
        db_table = "competence_skill_tree"
        verbose_name = "Скиллы"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stack = models.ForeignKey(Stacks, on_delete=models.CASCADE)
    level_of_knowledge = models.CharField(max_length=128)


class UserData(models.Model):
    class Meta:
        db_table = "user"
        verbose_name = "Данные о пользователе"

    login = models.CharField(max_length=128)
    firstname = models.CharField(max_length=128)
    middlename = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    photo = models.UUIDField()
    about_me = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    telegram_nick = models.CharField(max_length=128)
    hide_contacts = models.BooleanField()
    course = models.CharField(max_length=128)
    group = models.CharField(max_length=128)

    @staticmethod
    def get_data_from_db():
        courses2 = UserData.objects.all()
        data = []
        for course2 in courses2:
            data.append({
                'login': course2.login,
                'firstname': course2.firstname,
                'middlename': course2.middlename,
                'lastname': course2.lastname,
                'photo': course2.photo,
                'about_me': course2.about_me,
                'phone_number': course2.phone_number,
                'email': course2.email,
                'telegram_nick': course2.telegram_nick,
                'hide_contacts': course2.hide_contacts,
                'course': course2.course,
                'group': course2.group,
            })
        return data


class CompetenceExtracurricularCourses(models.Model):
    class Meta:
        db_table = "competence_extracurricular_courses"
        verbose_name = "Дополнительные курсы компетенции"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    organisation = models.CharField(max_length=200)
    certificate_number = models.CharField(max_length=100)

    @staticmethod
    def get_data_from_db():
        courses2 = CompetenceExtracurricularCourses.objects.all()
        data = []
        for course2 in courses2:
            data.append({
                'course_name': course2.name,
                'description': course2.organisation,
                'access_code': course2.certificate_number
            })
        return data


class Students(models.Model):
    class Meta:
        db_table = "students"
        verbose_name = "Студенты"

    course = models.IntegerField()
    admission_year = models.IntegerField()
    user_id = models.IntegerField()

    @staticmethod
    def get_data_from_db():
        courses = Students.objects.all()
        data = []
        for courseses in courses:
            data.append({
                'course': courseses.course,
                'admission_year': courseses.admission_year,
                'user_id': courseses.user_id
            })
        return data


class CompetenceScientificPublications(models.Model):
    class Meta:
        db_table = "competence_scientific_publications"
        verbose_name = "Компетентность научные публикации"

    name = models.CharField(max_length=150)
    year_of_issue = models.IntegerField()
    publication_level = models.CharField(max_length=50)
    journal = models.CharField(max_length=150)
    authors = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def get_data_from_db():
        courses3 = CompetenceScientificPublications.objects.all()
        data = []
        for courseses3 in courses3:
            data.append({
                'name': courseses3.name,
                'year_of_issue': courseses3.year_of_issue,
                'publication_level': courseses3.publication_level,
                'journal': courseses3.journal,
                'authors': courseses3.authors
            })
        return data
