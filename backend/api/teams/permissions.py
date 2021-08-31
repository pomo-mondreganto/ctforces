import api.permissions


class HasEditTeamPermission(api.permissions.HasPermissionMixin):
    permission_name = 'api.change_team'
    must_have_general_permission = False

    def has_permission(self, request, view):
        return True


class HasDeleteTeamPermission(api.permissions.HasPermissionMixin):
    permission_name = 'api.delete_team'
    must_have_general_permission = False

    def has_permission(self, request, view):
        return True
