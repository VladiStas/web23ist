from django.db import models


class Student(models.Model):
    course = models.IntegerField()
    group_id = models.IntegerField()
