from django.urls import re_path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from api.contests import views as api_contests_views
from api.posts import views as api_posts_views
from api.tasks import views as api_tasks_views
from api.teams import views as api_teams_views
from api.users import views as api_users_views

router = SimpleRouter()
router.register('users', api_users_views.UserViewSet)
router.register('teams', api_teams_views.TeamViewSet)
router.register('tasks', api_tasks_views.TaskViewSet)
router.register('task_tags', api_tasks_views.TaskTagViewSet)
router.register('task_files', api_tasks_views.TaskFileViewSet, basename='task_files')
router.register('task_hints', api_tasks_views.TaskHintViewSet)
router.register('posts', api_posts_views.PostViewSet)
router.register('contests', api_contests_views.ContestViewSet)
router.register('contest_participant_relationship', api_contests_views.ContestParticipantRelationshipViewSet)
router.register('contest_task_relationship', api_contests_views.ContestTaskRelationshipViewSet)

contests_router = NestedSimpleRouter(router, 'contests', lookup='contest')
contests_router.register('tasks', api_contests_views.ContestTaskViewSet)

urlpatterns = [
    re_path('^', include(router.urls)),
    re_path('^', include(contests_router.urls)),

    re_path('^register/$', api_users_views.UserCreateView.as_view(), name='registration_view'),

    re_path('^confirm_email/$',
            api_users_views.EmailConfirmationEndpointView.as_view(),
            name='email_confirmation_view'),

    re_path('^resend_confirmation/$',
            api_users_views.ActivationEmailResendView.as_view(),
            name='email_confirmation_resend_view'),

    re_path('^request_password_reset/$',
            api_users_views.PasswordResetRequestView.as_view(),
            name='password_reset_request_view'),

    re_path('^reset_password/$',
            api_users_views.PasswordResetEndpointView.as_view(),
            name='password_reset_view'),

    re_path('^login/$', api_users_views.LoginView.as_view(), name='login_view'),
    re_path('^logout/$', api_users_views.LogoutView.as_view(), name='logout_view'),

    re_path('^me/$', api_users_views.CurrentUserRetrieveUpdateView.as_view(), name='current_user'),

    re_path('^avatar_upload/$', api_users_views.AvatarUploadView.as_view(), name='avatar_upload_view'),
]
