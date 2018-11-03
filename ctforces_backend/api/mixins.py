from guardian.shortcuts import get_objects_for_user


class CustomPermissionsViewSetMixin:
    action_permission_classes = None

    def get_permissions(self):
        if self.action not in self.action_permission_classes:
            return super(CustomPermissionsViewSetMixin, self).get_permissions()
        return [permission() for permission in self.action_permission_classes[self.action]]


class CustomPermissionsQuerysetViewSetMixin:
    action_permissions_querysets = None
    klass = None

    def get_queryset(self):
        if self.action not in self.action_permissions_querysets:
            return super(CustomPermissionsQuerysetViewSetMixin, self).get_queryset()
        if not self.klass:
            raise AssertionError('Need to specify class to fetch permissions for (klass)')
        return get_objects_for_user(self.request.user, self.action_permissions_querysets[self.action], self.klass)
