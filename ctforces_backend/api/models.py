from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator
