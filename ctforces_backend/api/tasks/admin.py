from django.contrib import admin
from django.db.models import Count
from django.utils import timezone

from api import models as api_models


class TaskHintInlineAdmin(admin.TabularInline):
    model = api_models.TaskHint
    classes = ('collapse',)

    fieldsets = (
        (
            'Main info',
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


class CustomTaskAdmin(admin.ModelAdmin):
    inlines = (TaskHintInlineAdmin,)
    list_display = (
        'id',
        'name',
        'author',
        'flag',
        'cost',
        'solved_count',
        'is_published',
        'publication_time',
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
                    'name',
                    'description',
                    'author',
                    'flag',
                    'cost',
                ),
            }
        ),
        (
            'Publication',
            {
                'fields': (
                    'is_published',
                    'publication_time',
                ),
            }
        ),
        (
            'Other info',
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
        'solved_by',
        'tags',
    )

    readonly_fields = ('solved_count',)

    raw_id_fields = (
        'solved_by',
        'author',
    )

    @staticmethod
    def solved_count(obj):
        return obj.solved_count

    def get_queryset(self, request):
        return super(CustomTaskAdmin, self).get_queryset(request).annotate(
            solved_count=Count('solved_by')
        ).select_related('author')

    def publish(self, _request, queryset):
        queryset.update(is_published=True, publication_time=timezone.now())

    publish.short_description = "Publish selected tasks"

    def unpublish(self, _request, queryset):
        queryset.update(is_published=False)

    unpublish.short_description = "Unpublish selected tasks"

    actions = (
        'publish',
        'unpublish',
    )
