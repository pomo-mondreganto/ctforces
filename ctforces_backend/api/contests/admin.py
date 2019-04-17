from django.contrib import admin
from django.db.models import Value as V, Count, OuterRef
from django.db.models.functions import Coalesce
from guardian.admin import GuardedModelAdmin

from api import database_functions as api_database_functions
from api import models as api_models


class ContestTaskInlineAdmin(admin.TabularInline):
    classes = ('collapse',)
    model = api_models.ContestTaskRelationship
    fieldsets = (
        (
            'Main info',
            {
                'fields': (
                    'id',
                    'task',
                    'cost',
                    'ordering_number',
                ),
            },
        ),
        (
            'Other info',
            {
                'fields': (
                    'solved_count',
                )
            }
        )
    )

    readonly_fields = ('solved_count',)
    raw_id_fields = (
        'task',
    )

    @staticmethod
    def solved_count(obj):
        return obj.solved_count

    def get_queryset(self, request):
        return super(ContestTaskInlineAdmin, self).get_queryset(request).annotate(
            solved_count=Coalesce(
                api_database_functions.SubqueryCount(
                    api_models.ContestTaskParticipantSolvedRelationship.objects.filter(
                        contest_id=OuterRef('contest_id'),
                        task_id=OuterRef('task_id'),
                    )
                ),
                V(0),
            )
        )


class ContestParticipantInlineAdmin(admin.TabularInline):
    model = api_models.ContestParticipantRelationship
    classes = ('collapse',)
    fieldsets = (
        (
            'Main info',
            {
                'fields': (
                    'id',
                    'participant',
                    'last_solve',
                ),
            },
        ),
    )

    readonly_fields = (
        'last_solve',
    )

    raw_id_fields = (
        'participant',
    )


class CustomContestAdmin(GuardedModelAdmin):
    inlines = (
        ContestTaskInlineAdmin,
        ContestParticipantInlineAdmin,
    )

    list_display = (
        'id',
        'name',
        'author',
        'is_published',
        'is_running',
        'is_finished',
        'is_registration_open',
        'start_time',
        'end_time',
        'registered_count',
    )

    list_display_links = (
        'id',
        'name',
    )

    readonly_fields = (
        'registered_count',
    )

    fieldsets = (
        (
            'Main info',
            {
                'fields': (
                    'name',
                    'description',
                    'author',
                ),
            },
        ),
        (
            'Access',
            {
                'fields': (
                    'is_published',
                    'is_running',
                    'is_finished',
                    'is_registration_open',
                )
            },
        ),
        (
            'Dates',
            {
                'fields': (
                    'start_time',
                    'end_time',
                    'celery_start_task_id',
                    'celery_end_task_id',
                ),
                'classes': ('collapse',),
            },
        ),
        (
            'Auxiliary',
            {
                'fields': (
                    'is_rated',
                    'publish_tasks_after_finished',
                    'always_recalculate_rating',
                ),
                'classes': ('collapse',),
            },
        ),
    )

    raw_id_fields = (
        'participants',
        'author',
    )

    filter_horizontal = (
        'tasks',
        'participants',
    )

    @staticmethod
    def registered_count(obj):
        return obj.registered_count

    def get_queryset(self, request):
        return super(CustomContestAdmin, self).get_queryset(request).annotate(
            registered_count=Count('participants', distinct=True),
        ).prefetch_related('tasks', 'participants')


class InputFilter(admin.SimpleListFilter):
    def queryset(self, request, queryset):
        return super(InputFilter, self).queryset(request, queryset)

    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        return (),

    def choices(self, changelist):
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class UserIDFilter(InputFilter):
    parameter_name = 'participant_id'

    title = 'User id'

    def queryset(self, request, queryset):
        if self.value() is not None:
            user_id = self.value()
            return queryset.filter(
                participant_id=user_id,
            )


class ContestIDFilter(InputFilter):
    parameter_name = 'contest_id'

    title = 'Contest id'

    def queryset(self, request, queryset):
        if self.value() is not None:
            contest_id = self.value()
            return queryset.filter(
                contest_id=contest_id,
            )


class TaskIDFilter(InputFilter):
    parameter_name = 'task_id'

    title = 'Task id'

    def queryset(self, request, queryset):
        if self.value() is not None:
            task_id = self.value()
            return queryset.filter(
                task_id=task_id,
            )


class ContestTaskParticipantSolvedAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'participant',
        'contest',
        'task',
    )

    list_display_links = (
        'id',
    )

    list_filter = (
        UserIDFilter,
        TaskIDFilter,
        ContestIDFilter,
    )

    fieldsets = (
        (
            'Main info',
            {
                'fields': (
                    'id',
                    'participant',
                    'contest',
                    'task',
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return super(ContestTaskParticipantSolvedAdmin, self).get_queryset(request).select_related(
            'participant',
            'contest',
            'task',
        )
