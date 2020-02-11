from api.permissions import HasPermissionMixin, HasViewPermissionIfPublishedMixin


class HasContestTaskRelationshipPermission(HasPermissionMixin):
    permission_name = 'api.change_contest'

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True

        return request.user.has_perm(self.permission_name, obj.contest)


class HasEditContestPermission(HasPermissionMixin):
    permission_name = 'api.change_contest'


class HasCreateContestPermission(HasPermissionMixin):
    permission_name = 'api.add_contest'


class HasDeleteContestPermission(HasPermissionMixin):
    permission_name = 'api.delete_contest'


class HasViewContestPermission(HasViewPermissionIfPublishedMixin):
    permission_name = 'api.view_contest'

    def has_permission(self, request, view):
        return True
