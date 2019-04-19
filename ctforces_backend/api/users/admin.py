from django import forms
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.helpers import ActionForm
from django.contrib.auth.admin import UserAdmin
from django.db.models import Sum, Value as V, Q
from django.db.models.functions import Coalesce

from api import models as api_models


class UserAdminActionForm(ActionForm):
    contest_id = forms.IntegerField(required=False)


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


class CustomUserAdmin(UserAdmin):
    inlines = (
        ContestParticipantFullInlineAdmin,
    )

    action_form = UserAdminActionForm

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

    ordering = ('id',)

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
                    'has_participated_in_rated_contest',
                    'show_in_ratings',
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
        return super(CustomUserAdmin, self).get_queryset(request).prefetch_related(
            'groups', 'user_permissions'
        ).annotate(
            cost_sum=Coalesce(
                Sum(
                    'solved_tasks__cost',
                    filter=Q(solved_tasks__is_published=True),
                ),
                V(0),
            )
        )

    @staticmethod
    def cost_sum(obj):
        return obj.cost_sum

    def register_for_contest(self, request, queryset):
        contest_id = request.POST.get('contest_id')
        try:
            contest_id = int(contest_id)
        except ValueError:
            raise forms.ValidationError('Invalid contest_id')

        contest = api_models.Contest.objects.filter(id=contest_id).first()
        if not contest:
            raise forms.ValidationError('Invalid contest')

        already_registered = contest.participants.all()
        queryset = queryset.difference(already_registered)

        api_models.ContestParticipantRelationship.objects.bulk_create([
            api_models.ContestParticipantRelationship(
                contest=contest,
                participant=user,
            ) for user in queryset.all()
        ])
        self.message_user(
            request,
            'Successfully registered {0} users for contest <{1}:{2}>'.format(
                queryset.count(),
                contest_id,
                contest.name,
            ),
            messages.SUCCESS,
        )

    register_for_contest.short_description = 'Register selected users for contest'

    actions = (
        'register_for_contest',
    )
