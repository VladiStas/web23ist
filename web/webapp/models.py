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



