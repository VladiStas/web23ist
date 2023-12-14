from django.db import models
from django.urls import reverse


class User(models.Model):

    class Meta:
        managed = False
        db_table = "auth_user"
        verbose_name = "Пользователи"

    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)

    def get_url(self):
        return reverse('user', kwargs={'user_id': self.pk})

class Project(models.Model):

    class Meta:
        db_table = "projects"
        verbose_name = "Проекты"

    project_name = models.CharField(max_length=100)
    status = models.CharField(max_length=15)
    about_project = models.CharField(max_length=600)
    project_admin = models.IntegerField()

    def get_url(self):
        return reverse('project', kwargs={'project_id': self.pk})
    @staticmethod
    def get_data_from_db():
        projects = Project.objects.all()
        data = [{
            'project_name': project.project_name,
            'status': project.status,
            'about_project': project.about_project,
            'project_admin': project.project_admin
        } for project in projects]
        return data


class CompetenceSkillTree(models.Model):

    class Meta:
        db_table = "competence_skill_tree"
        verbose_name = "Скиллы"

    level_of_knowledge = models.CharField(max_length=128)


class UserData(models.Model):

    class Meta:
        db_table = "user"
        verbose_name = "Данные о пользователе"

    # competence = models.ForeignKey(CompetenceSkillTree, on_delete=models.CASCADE)

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

    # user = models.OneToOneField(CompetenceSkillTree, related_name='skill_tree', on_delete=models.CASCADE)


class CompetenceExtracurricularCourses(models.Model):
    class Meta:
        db_table = "competence_extracurricular_courses"
        verbose_name = "Дополнительные курсы компетенции"

    user_id = models.IntegerField()
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
