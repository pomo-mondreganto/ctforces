from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()
    email = models.EmailField('email address', blank=False, unique=True, null=False)

    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)


class Post(models.Model):
    author = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='posts', null=True, blank=True)
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(blank=False)
    is_published = models.BooleanField(default=False)
    is_main_page = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)
