from api import permissions as api_permissions


class HasEditTeamPermission(api_permissions.HasPermissionMixin):
    permission_name = 'api.change_team'


class HasDeleteTeamPermission(api_permissions.HasPermissionMixin):
    permission_name = 'api.delete_team'
