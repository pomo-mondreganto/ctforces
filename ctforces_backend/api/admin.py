from django.contrib import admin

from api import models as api_models
from api.contests import admin as api_contests_admin
from api.posts import admin as api_posts_admin
from api.tasks import admin as api_tasks_admin
from api.teams import admin as api_teams_admin
from api.users import admin as api_users_admin

admin.site.register(api_models.User, api_users_admin.CustomUserAdmin)
admin.site.register(api_models.Task, api_tasks_admin.TaskAdmin)
admin.site.register(api_models.TaskFile, api_tasks_admin.TaskFileFullAdmin)
admin.site.register(api_models.TaskTag, api_tasks_admin.TaskTagAdmin)
admin.site.register(api_models.Post, api_posts_admin.PostAdmin)
admin.site.register(api_models.Contest, api_contests_admin.ContestAdmin)
admin.site.register(api_models.Team, api_teams_admin.TeamAdmin)
