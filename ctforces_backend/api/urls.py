from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api import views as api_views

schema_view = get_schema_view(
    openapi.Info(
        title="CTForces API",
        default_version='v1',
        description="Schema of CTForces API. I suggest using schema-redoc/ version due to its beauty :3",
    ),
    validators=['flex'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path('^$', api_views.test_view, name='test_view'),
    re_path('^register/$', api_views.UserCreateView.as_view(), name='registration_view'),
    re_path('^confirm_email/$', api_views.EmailConfirmationEndpointView.as_view(), name='email_confirmation_view'),
    re_path('^login/$', api_views.LoginView.as_view(), name='login_view'),

    re_path(r'^schema_swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^schema_swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^schema_redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
