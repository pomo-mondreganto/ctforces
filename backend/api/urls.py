from django.urls import re_path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

import api.contests.views
import api.posts.views
import api.tasks.views
import api.teams.views
import api.users.views

router = SimpleRouter()
router.register('users', api.users.views.UserViewSet)
router.register('teams', api.teams.views.TeamViewSet)
router.register('tasks', api.tasks.views.TaskViewSet)
router.register('task_tags', api.tasks.views.TaskTagViewSet)
router.register('task_files', api.tasks.views.TaskFileViewSet, basename='task_files')
router.register('task_hints', api.tasks.views.TaskHintViewSet)
router.register('posts', api.posts.views.PostViewSet)
router.register('contests', api.contests.views.ContestViewSet)
router.register('contest_participant_relationship', api.contests.views.ContestParticipantRelationshipViewSet)
router.register('contest_task_relationship', api.contests.views.ContestTaskRelationshipViewSet)

contests_router = NestedSimpleRouter(router, 'contests', lookup='contest')
contests_router.register('tasks', api.contests.views.ContestTaskViewSet)

urlpatterns = [
    re_path('^', include(router.urls)),
    re_path('^', include(contests_router.urls)),

    re_path('^register/$', api.users.views.UserCreateView.as_view(), name='registration_view'),

    re_path('^confirm_email/$',
            api.users.views.EmailConfirmationEndpointView.as_view(),
            name='email_confirmation_view'),

    re_path('^resend_confirmation/$',
            api.users.views.ActivationEmailResendView.as_view(),
            name='email_confirmation_resend_view'),

    re_path('^request_password_reset/$',
            api.users.views.PasswordResetRequestView.as_view(),
            name='password_reset_request_view'),

    re_path('^reset_password/$',
            api.users.views.PasswordResetEndpointView.as_view(),
            name='password_reset_view'),

    re_path('^login/$', api.users.views.LoginView.as_view(), name='login_view'),
    re_path('^logout/$', api.users.views.LogoutView.as_view(), name='logout_view'),

    re_path('^me/$', api.users.views.CurrentUserRetrieveUpdateView.as_view(), name='current_user'),

    re_path('^avatar_upload/$', api.users.views.AvatarUploadView.as_view(), name='avatar_upload_view'),
]
