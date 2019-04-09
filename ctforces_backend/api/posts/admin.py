from django.utils import timezone
from guardian.admin import GuardedModelAdmin


class CustomPostAdmin(GuardedModelAdmin):
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
