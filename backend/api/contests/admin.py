from django import forms
from django.contrib import admin
from guardian.admin import GuardedModelAdmin

import api.models


class ContestTaskInlineAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if task := getattr(self.instance, 'task', None):
            self.fields['main_tag'].queryset = task.tags.all()


class ContestTaskInlineAdmin(admin.TabularInline):
    form = ContestTaskInlineAdminForm
    classes = ('collapse',)
    model = api.models.ContestTaskRelationship
    fieldsets = (
        (
            'General',
            {
                'fields': (
                    'id',
                    'task',
                    'main_tag',
                ),
            },
        ),
        (
            'Scoring',
            {
                'fields': (
                    'cost',
                    'min_cost',
                    'decay_value',
                ),
            },
        ),
        (
            'Other',
            {
                'fields': (
                    'solved_count',
                    'solved_by',
                    'chosen_for',
                )
            }
        )
    )

    readonly_fields = ('solved_count',)

    raw_id_fields = (
        'task',
        'solved_by',
        'chosen_for',
    )

    @staticmethod
    def solved_count(obj):
        return obj.solved_count

    def get_queryset(self, request):
        return super(ContestTaskInlineAdmin, self).get_queryset(request).with_solved_count()


class ContestParticipantInlineAdmin(admin.TabularInline):
    model = api.models.ContestParticipantRelationship
    classes = ('collapse',)
    fieldsets = (
        (
            'General',
            {
                'fields': (
                    'id',
                    'participant',
                    'registered_users',
                    'last_solve',
                    'opened_contest_at',
                    'randomized_tasks',
                ),
            },
        ),
    )

    readonly_fields = (
        'last_solve',
    )

    raw_id_fields = (
        'participant',
        'registered_users',
    )


class ContestAdmin(GuardedModelAdmin):
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
        'is_virtual',
        'start_time',
        'end_time',
        'registrations',
    )

    list_display_links = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )

    readonly_fields = (
        'registrations',
        'is_running',
        'is_finished',
    )

    fieldsets = (
        (
            'General',
            {
                'fields': (
                    'name',
                    'description',
                    'author',
                    'dynamic_scoring',
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
                    'public_scoreboard',
                )
            },
        ),
        (
            'Dates',
            {
                'fields': (
                    'start_time',
                    'end_time',
                    'celery_end_task_id',
                    'processed_end_task',
                ),
                'classes': ('collapse',),
            },
        ),
        (
            'Virtual',
            {
                'fields': (
                    'is_virtual',
                    'virtual_duration',
                ),
                'classes': ('collapse',),
            },
        ),
        (
            'Virtual',
            {
                'fields': (
                    'randomize_tasks',
                    'randomize_tasks_count',
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

    save_as = True

    @staticmethod
    def registrations(obj):
        return obj.registered_count

    def get_queryset(self, request):
        return super(ContestAdmin, self).get_queryset(request).with_participant_count().prefetch_related(
            'tasks',
            'participants',
        )


class InputFilter(admin.SimpleListFilter):
    def queryset(self, request, queryset):
        return super(InputFilter, self).queryset(request, queryset)

    template = 'admin_templates/input_filter.html'

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


class CPRHelperAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'contest',
        'user',
        'cpr',
    )

    list_display_links = (
        'id',
    )

    list_filter = (
        UserIDFilter,
        ContestIDFilter,
    )

    list_select_related = (
        'user',
        'contest',
        'cpr',
    )

    raw_id_fields = (
        'user',
        'contest',
        'cpr',
    )

    fieldsets = (
        (
            'General',
            {
                'fields': (
                    'id',
                    'user',
                    'contest',
                    'cpr',
                ),
            },
        ),
    )
