from rest_framework import permissions


class HasPermissionMixin(permissions.BasePermission):
    permission_name = None

    def has_object_permission(self, request, view, obj):
        if self.permission_name is None:
            raise AssertionError('You must specify permission_name')

        return request.user.is_admin or request.user.has_perm(self.permission_name, obj)

    def has_permission(self, request, view):
        if self.permission_name is None:
            raise AssertionError('You must specify permission_name')

        if request.user.is_admin:
            return True

        return request.user.has_perm(self.permission_name)


class HasPermissionOrReadOnlyMixin(permissions.BasePermission):
    permission_name = None

    def has_object_permission(self, request, view, obj):
        if self.permission_name is None:
            raise AssertionError('You must specify permission_name')

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_admin:
            return True

        return request.user.has_perm(self.permission_name, obj)

    def has_permission(self, request, view):
        if self.permission_name is None:
            raise AssertionError('You must specify permission_name')

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_admin:
            return True

        return request.user.has_perm(self.permission_name)


class HasViewPermissionIfPublishedMixin(HasPermissionMixin):
    is_published_field_name = 'is_published'

    def has_object_permission(self, request, view, obj):
        if self.permission_name is None:
            raise AssertionError('You must specify permission_name')

        if getattr(obj, self.is_published_field_name):
            return True

        if request.user.is_admin:
            return True

        return request.user.has_perm(self.permission_name, obj)
