from django.urls import re_path

from api import views as api_views

urlpatterns = [
    re_path('^$', api_views.test_view, name='test_view')
]
