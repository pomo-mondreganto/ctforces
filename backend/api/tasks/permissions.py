from api.permissions import (
    HasPermissionMixin,
    HasPermissionOrReadOnlyMixin,
    HasViewPermissionIfPublishedMixin,
)


class HasEditTaskPermissionOrReadOnly(HasPermissionOrReadOnlyMixin):
    permission_name = 'api.change_task'
    must_have_general_permission = False


class HasEditTaskPermission(HasPermissionMixin):
    permission_name = 'api.change_task'
    must_have_general_permission = False


class HasCreateTaskPermissionOrReadOnly(HasPermissionOrReadOnlyMixin):
    permission_name = 'api.add_task'
    must_have_general_permission = True


class HasCreateTaskPermission(HasPermissionMixin):
    permission_name = 'api.add_task'
    must_have_general_permission = True


class HasDeleteTaskPermissionOrReadOnly(HasPermissionOrReadOnlyMixin):
    permission_name = 'api.delete_task'
    must_have_general_permission = False


class HasDeleteTaskPermission(HasPermissionMixin):
    permission_name = 'api.delete_task'
    must_have_general_permission = False


class HasCreateTaskFilePermission(HasPermissionMixin):
    permission_name = 'api.add_taskfile'
    must_have_general_permission = True


class HasCreateTaskFilePermissionOrReadOnly(HasPermissionOrReadOnlyMixin):
    permission_name = 'api.add_taskfile'
    must_have_general_permission = True


class HasViewTaskPermission(HasViewPermissionIfPublishedMixin):
    permission_name = 'api.view_task'
    must_have_general_permission = False

    def has_object_permission(self, request, view, obj):
        if obj.show_on_main_page:
            return True

        return super(HasViewTaskPermission, self).has_object_permission(request, view, obj)


class HasEditTaskHintsPermission(HasPermissionMixin):
    permission_name = 'api.change_task'
    must_have_general_permission = False

    def has_object_permission(self, request, view, obj):
        return super(HasEditTaskHintsPermission, self).has_object_permission(request, view, obj.task)


class HasViewTaskHintPermission(HasViewPermissionIfPublishedMixin):
    permission_name = 'api.view_taskhint'
    must_have_general_permission = False
