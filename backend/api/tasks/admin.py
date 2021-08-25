from django.contrib import admin
from django.db.models import Count
from django.utils import timezone
from guardian.admin import GuardedModelAdmin

from api.models import (
    TaskHint,
    TaskFile,
)


class TaskHintInlineAdmin(admin.TabularInline):
    model = TaskHint
    classes = ('collapse',)

    fieldsets = (
        (
            'General',
            {
                'fields': (
                    'id',
                    'author',
                    'body',
                    'is_published',
                ),
            },
        ),
    )


class TaskFileInlineAdmin(admin.TabularInline):
    model = TaskFile
    classes = ('collapse',)

    fieldsets = (
        (
            'General',
            {
                'fields': (
                    'id',
                    'owner',
                    'name',
                    'upload_time',
                    'file_field',
                ),
            },
        ),
    )

    readonly_fields = ('upload_time',)
    raw_id_fields = ('owner',)


class TaskAdmin(GuardedModelAdmin):
    inlines = (TaskHintInlineAdmin, TaskFileInlineAdmin)
    list_display = (
        'id',
        'name',
        'author',
        'flag',
        'cost',
        'solved_count',
        'show_on_main_page',
        'publication_time',
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
                    'description',
                    'author',
                    'flag',
                    'cost',
                ),
            }
        ),
        (
            'Visibility',
            {
                'fields': (
                    'is_published',
                    'show_on_main_page',
                    'publication_time',
                ),
            }
        ),
        (
            'Other',
            {
                'fields': (
                    'solved_count',
                    'solved_by',
                    'tags',
                ),
                'classes': ('collapse',),
            }
        ),
    )

    filter_horizontal = (
        'tags',
    )

    readonly_fields = ('solved_count',)

    raw_id_fields = (
        'solved_by',
        'author',
    )

    search_fields = (
        'name',
        'flag',
    )

    list_filter = (
        'tags',
    )

    @staticmethod
    def solved_count(obj):
        return obj.solved_count

    def get_queryset(self, request):
        return super(TaskAdmin, self).get_queryset(request).annotate(
            solved_count=Count('solved_by')
        ).select_related('author')

    def publish(self, _request, queryset):
        queryset.update(
            show_on_main_page=True,
            is_published=True,
            publication_time=timezone.now(),
        )

    publish.short_description = "Publish selected tasks to main page"

    def unpublish_full(self, _request, queryset):
        queryset.update(
            is_published=False,
            show_on_main_page=False,
        )

    unpublish_full.short_description = "Unpublish selected tasks both from main page and user"

    def unpublish_main(self, _request, queryset):
        queryset.update(
            show_on_main_page=False,
        )

    unpublish_main.short_description = "Unpublish selected tasks from main page only"

    actions = (
        'publish',
        'unpublish_full',
        'unpublish_main',
    )


class TaskFileAdmin(GuardedModelAdmin):
    model = TaskFile

    list_display = (
        'id',
        'name',
        'owner',
        'upload_time',
    )

    list_display_links = (
        'id',
        'name',
    )

    readonly_fields = ('upload_time',)
    raw_id_fields = ('owner',)


class TaskTagAdmin(GuardedModelAdmin):
    list_display = (
        'id',
        'name',
    )

    list_display_links = (
        'id',
        'name',
    )


class SubmissionAdmin(GuardedModelAdmin):
    list_display = (
        'id',
        'user',
        'task',
        'success',
        'flag',
        'participant',
        'contest',
    )

    list_display_links = (
        'id',
        'user',
    )

    list_select_related = (
        'user',
        'task',
        'participant',
        'contest',
    )

    raw_id_fields = (
        'user',
        'task',
        'participant',
        'contest',
    )
