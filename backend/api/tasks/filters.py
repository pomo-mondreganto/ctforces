import django_filters
from django.db.models import Q

import api.models


class TaskTagFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = api.models.TaskTag
        fields = ('name',)


class TaskQFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value is None:
            return qs

        return qs.filter(
            Q(tags__name__icontains=value) |
            Q(name__icontains=value) |
            Q(author__username__icontains=value)
        )


class TaskTagFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value is None:
            return qs

        return qs.filter(tags__name=value)


class TaskFilterSet(django_filters.FilterSet):
    tag = TaskTagFilter()
    q = TaskQFilter()

    class Meta:
        model = api.models.Task
        fields = ('tag', 'q')
