class CustomPermissionsViewSetMixin:
    action_permission_classes = None

    def get_permissions(self):
        permissions = super(CustomPermissionsViewSetMixin, self).get_permissions()
        if self.action in self.action_permission_classes:
            permissions += (permission() for permission in self.action_permission_classes[self.action])
        return permissions


class ReadOnlySerializerMixin:
    def create(self, *args, **kwargs):
        raise NotImplementedError('Trying to call create of a read-only serializer')

    def update(self, *args, **kwargs):
        raise NotImplementedError('Trying to call update of a read-only serializer')
