from api import permissions as api_permissions


class HasEditPostPermission(api_permissions.HasPermissionMixin):
    permission_name = 'api.change_post'


class HasEditPostPermissionOrReadOnly(api_permissions.HasPermissionOrReadOnlyMixin):
    permission_name = 'api.change_post'


class HasViewPostPermission(api_permissions.HasViewPermissionIfPublishedMixin):
    permission_name = 'api.view_post'

    def has_permission(self, request, view):
        return True
