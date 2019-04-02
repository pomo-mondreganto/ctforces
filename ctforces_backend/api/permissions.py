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


class HasViewPermissionIfPublishedMixin(HasPermissionMixin):
    is_published_field_name = 'is_published'

    def has_object_permission(self, request, view, obj):
        if self.permission_name is None:
            raise AssertionError('You must specify permission_name')

        return getattr(obj, self.is_published_field_name) or request.user.has_perm(self.permission_name, obj)


class HasContestTaskRelationshipPermission(HasPermissionMixin):
    permission_name = 'change_contest'

    def has_object_permission(self, request, view, obj):
        return request.user.has_perm(self.permission_name, obj.contest)


class HasEditTaskPermissionOrReadOnly(HasPermissionOrReadOnlyMixin):
    permission_name = 'change_task'


class HasEditTaskPermission(HasPermissionMixin):
    permission_name = 'change_task'


class HasCreateTaskPermissionOrReadOnly(HasPermissionOrReadOnlyMixin):
    permission_name = 'add_task'


class HasCreateTaskPermission(HasPermissionMixin):
    permission_name = 'add_task'


class HasDeleteTaskPermissionOrReadOnly(HasPermissionOrReadOnlyMixin):
    permission_name = 'delete_task'


class HasDeleteTaskPermission(HasPermissionMixin):
    permission_name = 'delete_task'


class HasCreateTaskFilePermission(HasPermissionMixin):
    permission_name = 'add_taskfile'


class HasCreateTaskFilePermissionOrReadOnly(HasPermissionOrReadOnlyMixin):
    permission_name = 'add_taskfile'


class HasEditPostPermission(HasPermissionMixin):
    permission_name = 'change_post'


class HasEditPostPermissionOrReadOnly(HasPermissionOrReadOnlyMixin):
    permission_name = 'change_post'


class HasEditContestPermission(HasPermissionMixin):
    permission_name = 'change_contest'


class HasCreateContestPermission(HasPermissionMixin):
    permission_name = 'add_contest'


class HasDeleteContestPermission(HasPermissionMixin):
    permission_name = 'delete_contest'


class HasViewTaskPermission(HasViewPermissionIfPublishedMixin):
    permission_name = 'view_task'


class HasViewPostPermission(HasViewPermissionIfPublishedMixin):
    permission_name = 'view_post'


class HasViewContestPermission(HasViewPermissionIfPublishedMixin):
    permission_name = 'view_contest'


class HasModifyTaskHintsPermission(HasPermissionMixin):
    permission_name = 'change_task'

    def has_object_permission(self, request, view, obj):
        return request.user.has_perm(self.permission_name, obj.task)


class HasViewTaskHintPermission(HasViewPermissionIfPublishedMixin):
    permission_name = 'view_taskhint'
