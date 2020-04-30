import django_filters

import api.models


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='istartswith')
    ordering = django_filters.OrderingFilter(
        fields=(
            ('rating', 'rating'),
            ('cost_sum', 'cost_sum'),
            ('last_solve', 'last_solve'),
        ),
    )

    class Meta:
        model = api.models.User
        fields = ['username']
