import api.permissions


class HasEditPostPermission(api.permissions.HasPermissionMixin):
    permission_name = 'api.change_post'
    must_have_general_permission = False


class HasEditPostPermissionOrReadOnly(api.permissions.HasPermissionOrReadOnlyMixin):
    permission_name = 'api.change_post'
    must_have_general_permission = False


class HasViewPostPermission(api.permissions.HasViewPermissionIfPublishedMixin):
    permission_name = 'api.view_post'
    must_have_general_permission = False

    def has_object_permission(self, request, view, obj):
        if obj.show_on_main_page:
            return True

        return super(HasViewPostPermission, self).has_object_permission(request, view, obj)
