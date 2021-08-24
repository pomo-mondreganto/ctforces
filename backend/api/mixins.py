from guardian.shortcuts import get_objects_for_user


class CustomPermissionsViewSetMixin:
    action_permission_classes = None

    def get_permissions(self):
        permissions = super(CustomPermissionsViewSetMixin, self).get_permissions()
        if self.action in self.action_permission_classes:
            permissions += (permission() for permission in self.action_permission_classes[self.action])
        return permissions


class CustomPermissionsQuerysetViewSetMixin:
    action_permissions_querysets = None
    klass = None

    def get_queryset(self):
        assert self.klass is not None, 'klass field is required for CustomPermissionsQuerysetViewSetMixin'

        if self.action not in self.action_permissions_querysets:
            return super(CustomPermissionsQuerysetViewSetMixin, self).get_queryset()

        return get_objects_for_user(self.request.user, self.action_permissions_querysets[self.action], self.klass)


class ReadOnlySerializerMixin:
    def create(self, *args, **kwargs):
        raise NotImplementedError('Trying to call create of a read-only serializer')

    def update(self, *args, **kwargs):
        raise NotImplementedError('Trying to call update of a read-only serializer')
