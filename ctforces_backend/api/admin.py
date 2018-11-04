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


admin.site.register(api_models.User, CustomUserAdmin)
admin.site.register(api_models.Task, CustomTaskAdmin)
