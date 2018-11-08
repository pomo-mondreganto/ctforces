from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Sum, Value as V, Count
from django.db.models.functions import Coalesce
from django.utils import timezone

from api import models as api_models


class CustomUserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'last_solve',
        'hide_personal_info',
        'rating',
        'max_rating',
        'date_joined',
    )

    list_display_links = (
        'id',
        'username',
    )

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'password',
                ),
            }
        ),
        (
            'Personal information',
            {
                'fields': (
                    'first_name',
                    'last_name',
                ),
            }
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            }
        ),
        (
            'Ranking',
            {
                'fields': (
                    'rating',
                    'max_rating',
                    'cost_sum',
                ),
            }
        ),
        (
            'Dates',
            {
                'fields': (
                    'date_joined',
                    'updated_at',
                    'last_solve',
                ),
                'classes': ('collapse',),
            }
        ),
        (
            'Other info',
            {
                'fields': (
                    'avatar',
                ),
                'classes': ('collapse',),
            }
        ),
    )

    readonly_fields = ('cost_sum', 'updated_at')

    filter_horizontal = (
        'groups',
        'user_permissions',
    )

    def get_queryset(self, request):
        return super(CustomUserAdmin, self).get_queryset(request) \
            .prefetch_related('groups', 'user_permissions') \
            .annotate(cost_sum=Coalesce(Sum('solved_tasks__cost'), V(0)))

    @staticmethod
    def cost_sum(obj):
        return obj.cost_sum


class CustomTaskAdmin(admin.ModelAdmin):
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
        'tags',
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


class CustomPostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'is_published',
        'show_on_main_page',
        'created_at',
        'updated_at',
    )

    list_display_links = (
        'id',
        'title',
    )

    fieldsets = (
        (
            'Main info',
            {
                'fields': (
                    'title',
                    'body',
                    'author',
                ),
            }
        ),
        (
            'Publication info',
            {
                'fields': (
                    'is_published',
                    'show_on_main_page',
                ),
            }
        ),
        (
            'Dates',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                ),
            }
        ),
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    raw_id_fields = (
        'author',
    )

    def get_queryset(self, request):
        return super(CustomPostAdmin, self).get_queryset(request).select_related('author')

    def publish(self, _request, queryset):
        queryset.update(is_published=True, publication_time=timezone.now())

    publish.short_description = "Publish selected posts"

    def unpublish(self, _request, queryset):
        queryset.update(is_published=False)

    unpublish.short_description = "Unpublish selected posts"

    def add_to_main_page(self, _request, queryset):
        queryset.update(show_on_main_page=True)

    add_to_main_page.short_description = "Add selected posts to main page"

    def remove_from_main_page(self, _request, queryset):
        queryset.update(show_on_main_page=False)

    remove_from_main_page.short_description = "Remove selected posts from main page"

    actions = (
        'publish',
        'unpublish',
        'add_to_main_page',
        'remove_from_main_page',
    )


class ContestTaskInlineAdmin(admin.TabularInline):
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
                    'solved',
                )
            }
        )
    )

    readonly_fields = ('solved_count',)
    raw_id_fields = (
        'task',
        'solved',
    )

    @staticmethod
    def solved_count(obj):
        return obj.solved_count

    def get_queryset(self, request):
        return super(ContestTaskInlineAdmin, self).get_queryset(request).annotate(
            solved_count=Count(
                'solved',
                distinct=True,
            ),
        )


class CustomContestAdmin(admin.ModelAdmin):
    inlines = (ContestTaskInlineAdmin,)

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
            },
        ),
    )

    raw_id_fields = (
        'participants',
        'author',
    )

    filter_horizontal = (
        'tasks',
    )

    @staticmethod
    def registered_count(obj):
        return obj.registered_count

    def get_queryset(self, request):
        return super(CustomContestAdmin, self).get_queryset(request).annotate(
            registered_count=Count('participants', distinct=True),
        )


admin.site.register(api_models.User, CustomUserAdmin)
admin.site.register(api_models.Task, CustomTaskAdmin)
admin.site.register(api_models.Post, CustomPostAdmin)
admin.site.register(api_models.Contest, CustomContestAdmin)
