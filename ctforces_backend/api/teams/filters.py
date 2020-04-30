import django_filters

import api.models


class TeamFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')
    ordering = django_filters.OrderingFilter(
        fields=(
            ('rating', 'rating'),
        ),
    )

    class Meta:
        model = api.models.Team
        fields = ['name']
