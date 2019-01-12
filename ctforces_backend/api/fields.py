from guardian.shortcuts import get_objects_for_user
from rest_framework.serializers import PrimaryKeyRelatedField


class CurrentUserFilteredPKRF(PrimaryKeyRelatedField):
    def __init__(self, filter_field_name, **kwargs):
        super(CurrentUserFilteredPKRF, self).__init__(**kwargs)
        self.filter_field_name = filter_field_name

    def get_queryset(self):
        qs = super(CurrentUserFilteredPKRF, self).get_queryset()
        return qs.filter(**{self.filter_field_name: self.context['request'].user})


class CurrentUserPermissionsFilteredPKRF(PrimaryKeyRelatedField):
    def __init__(self, perms, **kwargs):
        super(CurrentUserPermissionsFilteredPKRF, self).__init__(**kwargs)
        self.perms = perms

    def get_queryset(self):
        qs = super(CurrentUserPermissionsFilteredPKRF, self).get_queryset()
        return get_objects_for_user(
            user=self.context['request'].user,
            klass=qs,
            perms=self.perms,
        )
