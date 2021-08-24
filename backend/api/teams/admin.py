from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from api import models as api_models


class ContestParticipantInlineAdmin(admin.TabularInline):
    model = api_models.ContestParticipantRelationship
    classes = ('collapse',)

    fieldsets = (
        (
            'General',
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
        ContestParticipantInlineAdmin,
    )

    list_display = (
        'id',
        'name',
        'captain',
        'created_at',
    )

    list_display_links = (
        'id',
        'name',
    )

    fieldsets = (
        (
            'General',
            {
                'fields': (
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
