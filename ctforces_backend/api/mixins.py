class CustomPermissionsViewSetMixin:
    action_permission_classes = None

    def get_permissions(self):
        if self.action not in self.action_permission_classes:
            return [permission() for permission in self.permission_classes]
        return [permission() for permission in self.action_permission_classes[self.action]]
