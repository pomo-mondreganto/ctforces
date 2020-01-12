from django.contrib import admin

from api import models as api_models
from api.contests import admin as api_contests_admin
from api.posts import admin as api_posts_admin
from api.tasks import admin as api_tasks_admin
from api.users import admin as api_users_admin

admin.site.register(api_models.User, api_users_admin.CustomUserAdmin)
admin.site.register(api_models.Task, api_tasks_admin.CustomTaskAdmin)
admin.site.register(api_models.TaskFile, api_tasks_admin.TaskFileFullAdmin)
admin.site.register(api_models.Post, api_posts_admin.CustomPostAdmin)
admin.site.register(api_models.Contest, api_contests_admin.CustomContestAdmin)
