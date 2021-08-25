from django.contrib import admin

import api.contests.admin
import api.models
import api.posts.admin
import api.tasks.admin
import api.teams.admin
import api.users.admin

admin.site.register(api.models.User, api.users.admin.CustomUserAdmin)
admin.site.register(api.models.Task, api.tasks.admin.TaskAdmin)
admin.site.register(api.models.TaskFile, api.tasks.admin.TaskFileAdmin)
admin.site.register(api.models.TaskTag, api.tasks.admin.TaskTagAdmin)
admin.site.register(api.models.Submission, api.tasks.admin.SubmissionAdmin)
admin.site.register(api.models.Post, api.posts.admin.PostAdmin)
admin.site.register(api.models.Contest, api.contests.admin.ContestAdmin)
admin.site.register(api.models.Team, api.teams.admin.TeamAdmin)
