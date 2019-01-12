from rest_framework.serializers import PrimaryKeyRelatedField


class CurrentUserFilteredPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    def __init__(self, filter_field_name, **kwargs):
        super(CurrentUserFilteredPrimaryKeyRelatedField, self).__init__(**kwargs)
        self.filter_field_name = filter_field_name

    def get_queryset(self):
        qs = super(CurrentUserFilteredPrimaryKeyRelatedField, self).get_queryset()
        return qs.filter(**{self.filter_field_name: self.context['request'].user})
