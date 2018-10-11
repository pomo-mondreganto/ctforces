from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api import models as api_models

admin.site.register(api_models.User, UserAdmin)
