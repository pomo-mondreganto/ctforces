from api import permissions as api_permissions


class HasEditTaskPermissionOrReadOnly(api_permissions.HasPermissionOrReadOnlyMixin):
    permission_name = 'api.change_task'


class HasEditTaskPermission(api_permissions.HasPermissionMixin):
    permission_name = 'api.change_task'


class HasCreateTaskPermissionOrReadOnly(api_permissions.HasPermissionOrReadOnlyMixin):
    permission_name = 'api.add_task'


class HasCreateTaskPermission(api_permissions.HasPermissionMixin):
    permission_name = 'api.add_task'


class HasDeleteTaskPermissionOrReadOnly(api_permissions.HasPermissionOrReadOnlyMixin):
    permission_name = 'api.delete_task'


class HasDeleteTaskPermission(api_permissions.HasPermissionMixin):
    permission_name = 'api.delete_task'


class HasCreateTaskFilePermission(api_permissions.HasPermissionMixin):
    permission_name = 'api.add_taskfile'


class HasCreateTaskFilePermissionOrReadOnly(api_permissions.HasPermissionOrReadOnlyMixin):
    permission_name = 'api.add_taskfile'


class HasViewTaskPermission(api_permissions.HasViewPermissionIfPublishedMixin):
    permission_name = 'api.view_task'

    def has_object_permission(self, request, view, obj):
        if obj.show_on_main_page:
            return True

        return super(HasViewTaskPermission, self).has_object_permission(request, view, obj)


class HasEditTaskHintsPermission(api_permissions.HasPermissionMixin):
    permission_name = 'api.change_task'

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True

        return request.user.has_perm(self.permission_name, obj.task)


class HasViewTaskHintPermission(api_permissions.HasViewPermissionIfPublishedMixin):
    permission_name = 'api.view_taskhint'
