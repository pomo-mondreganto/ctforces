from api import permissions as api_permissions


class HasContestTaskRelationshipPermission(api_permissions.HasPermissionMixin):
    permission_name = 'api.change_contest'

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True

        return request.user.has_perm(self.permission_name, obj.contest)


class HasEditContestPermission(api_permissions.HasPermissionMixin):
    permission_name = 'api.change_contest'


class HasCreateContestPermission(api_permissions.HasPermissionMixin):
    permission_name = 'api.add_contest'


class HasDeleteContestPermission(api_permissions.HasPermissionMixin):
    permission_name = 'api.delete_contest'


class HasViewContestPermission(api_permissions.HasViewPermissionIfPublishedMixin):
    permission_name = 'api.view_contest'

    def has_permission(self, request, view):
        return True
