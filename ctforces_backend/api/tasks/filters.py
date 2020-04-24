import django_filters

import api.models


class TaskTagFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = api.models.TaskTag
        fields = ['name']
