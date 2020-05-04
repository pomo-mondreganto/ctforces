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
    default_error_messages = {
        'required': 'This field is required.',
        'does_not_exist': 'Invalid pk "{pk_value}" - object does not exist or you have no access to it.',
        'incorrect_type': 'Incorrect type. Expected pk value, received {data_type}.',
    }

    def __init__(self, perms, additional_queryset=None, **kwargs):
        super(CurrentUserPermissionsFilteredPKRF, self).__init__(**kwargs)
        self.perms = perms
        self.additional_queryset = additional_queryset

    def get_queryset(self):
        qs = super(CurrentUserPermissionsFilteredPKRF, self).get_queryset()
        qs = get_objects_for_user(
            user=self.context['request'].user,
            klass=qs,
            perms=self.perms,
        )
        if self.additional_queryset:
            qs = (qs | self.additional_queryset).distinct()
        return qs
