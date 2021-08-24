from rest_framework import permissions


class HasPermissionMixin(permissions.BasePermission):
    permission_name = None
    must_have_general_permission = True

    def has_permission(self, request, view):
        assert self.permission_name is not None, 'permission_name is required'

        if not self.must_have_general_permission:
            return True

        if not request.user:
            return False

        return request.user.is_admin or request.user.has_perm(self.permission_name)

    def has_object_permission(self, request, view, obj):
        assert self.permission_name is not None, 'permission_name is required'

        if not request.user:
            return False

        return request.user.is_admin or request.user.has_perm(self.permission_name, obj)


class HasPermissionOrReadOnlyMixin(HasPermissionMixin):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super(HasPermissionOrReadOnlyMixin, self).has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super(HasPermissionOrReadOnlyMixin, self).has_object_permission(request, view, obj)


class HasViewPermissionIfPublishedMixin(HasPermissionMixin):
    is_published_field_name = 'is_published'

    def has_object_permission(self, request, view, obj):
        assert self.permission_name is not None, 'permission_name is required'

        if getattr(obj, self.is_published_field_name):
            return True

        if not request.user:
            return False

        return request.user.is_admin or request.user.has_perm(self.permission_name, obj)
