from django.db import models


class user(models.Model):
    login = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    firstname = models.CharField(max_length=128)
    middlename = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    photo = models.UUIDField()
    about_me = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    telegram_nick = models.CharField(max_length=128)
    hide_contacts = models.BooleanField()
