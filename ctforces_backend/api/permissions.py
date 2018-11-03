from rest_framework import permissions


class HasPermissionMixin(permissions.BasePermission):
    permission_name = None

    def has_object_permission(self, request, view, obj):
        if self.permission_name is None:
            raise AssertionError('You must specify permission_name')

        return request.user.has_perm(self.permission_name, obj)

    def has_permission(self, request, view):
        if self.permission_name is None:
            raise AssertionError('You must specify permission_name')

        return request.user.has_perm(self.permission_name)


class HasPermissionOrReadOnlyMixin(permissions.BasePermission):
    permission_name = None

    def has_object_permission(self, request, view, obj):
        if self.permission_name is None:
            raise AssertionError('You must specify permission_name')

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.has_perm(self.permission_name, obj)

    def has_permission(self, request, view):
        if self.permission_name is None:
            raise AssertionError('You must specify permission_name')

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.has_perm(self.permission_name)


class HasEditTaskPermissionOrReadOnly(HasPermissionOrReadOnlyMixin):
    permission_name = 'edit_task'


class HasEditTaskPermission(HasPermissionMixin):
    permission_name = 'edit_task'


class HasCreateTaskPermissionOrReadOnly(HasPermissionOrReadOnlyMixin):
    permission_name = 'create_task'


class HasCreateTaskPermission(HasPermissionMixin):
    permission_name = 'create_task'


class HasDeleteTaskPermissionOrReadOnly(HasPermissionOrReadOnlyMixin):
    permission_name = 'delete_task'


class HasDeleteTaskPermission(HasPermissionMixin):
    permission_name = 'delete_task'


class HasCreateFilePermission(HasPermissionMixin):
    permission_name = 'create_file'
