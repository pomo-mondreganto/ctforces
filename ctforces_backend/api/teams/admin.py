from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from api import models as api_models


class ContestParticipantFullInlineAdmin(admin.TabularInline):
    model = api_models.ContestParticipantRelationship
    classes = ('collapse',)

    fieldsets = (
        (
            'Main info',
            {
                'fields': (
                    'id',
                    'last_solve',
                    'delta',
                    'contest',
                    'has_opened_contest',
                ),
            },
        ),
    )

    readonly_fields = (
        'delta',
        'last_solve',
        'contest',
    )

    raw_id_fields = (
        'contest',
    )


class TeamAdmin(GuardedModelAdmin):
    inlines = (
        ContestParticipantFullInlineAdmin,
    )

    list_display = (
        'id',
        'name',
        'created_at',
    )

    list_display_links = (
        'id',
        'name',
    )

    fieldsets = (
        (
            'Main info',
            {
                'fields': (
                    # 'id',
                    'name',
                    'join_token',
                    'captain',
                    'participants',
                ),
            }
        ),
        (
            'Dates',
            {
                'fields': (
                    'created_at',
                ),
            }
        ),
    )

    raw_id_fields = (
        'captain',
        'participants',
    )

    readonly_fields = (
        'created_at',
    )

    def get_queryset(self, request):
        return super(TeamAdmin, self).get_queryset(request).select_related('captain')
