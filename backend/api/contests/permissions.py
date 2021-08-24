from api.permissions import HasPermissionMixin, HasViewPermissionIfPublishedMixin


def get_submission_ratelimit_key(_group, viewset):
    return str(viewset.request.user.id)


class HasContestTaskRelationshipPermission(HasPermissionMixin):
    permission_name = 'api.change_contest'
    must_have_general_permission = False

    def has_object_permission(self, request, view, obj):
        return super(HasContestTaskRelationshipPermission, self).has_object_permission(request, view, obj.contest)


class HasEditContestPermission(HasPermissionMixin):
    permission_name = 'api.change_contest'
    must_have_general_permission = False


class HasCreateContestPermission(HasPermissionMixin):
    permission_name = 'api.add_contest'
    must_have_general_permission = True


class HasDeleteContestPermission(HasPermissionMixin):
    permission_name = 'api.delete_contest'
    must_have_general_permission = False


class HasViewContestPermission(HasViewPermissionIfPublishedMixin):
    permission_name = 'api.view_contest'
    must_have_general_permission = False
