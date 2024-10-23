## Copyright 2021, J. Donald Tillman.  All rights reserverd.

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import os

class BayProgUserManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, about='', image=None, password=None):
        if not email:
            raise ValueError('Email is required')
        user = self.model(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname,
            about=about,
            image=image)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname, lastname, about='', image=None, password=None):
        user = self.create_user(
            email=email,
            firstname=firstname,
            lastname=lastname,
            about=about,
            image=image,
            password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class BayProgUser(AbstractBaseUser, PermissionsMixin):
    def imagepath(instance, filename):
        ext = os.path.splitext(filename)[-1]
        uid = instance.id
        return f'bayproguser/userphotos/user{uid}{ext}'

    email = models.EmailField('Email', max_length=64, unique=True)
    firstname = models.CharField('First Name', max_length=64)
    lastname = models.CharField('Last Name', max_length=64)
    about = models.TextField('Bio', blank=True, default='') 
    image = models.ImageField('Photo', upload_to=imagepath, blank=True)
    datejoined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = BayProgUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    def get_full_name(self):
        return self.firstname + ' ' + self.lastname

    def get_short_name(self):
        return self.firstname

    def __str__(self):
        return self.email

    def has_perm(self, perm, object=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
