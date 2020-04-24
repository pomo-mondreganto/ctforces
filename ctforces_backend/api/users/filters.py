import django_filters

import api.models


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = api.models.User
        fields = ['username']
