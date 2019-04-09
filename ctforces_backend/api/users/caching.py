from django.utils.encoding import force_text
from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.constructors import (
    KeyConstructor
)

from api import models as api_models


class UpdatedAtModelKeyBit(bits.KeyBitBase):

    def __init__(self, updated_at_field_name='updated_at'):
        super(UpdatedAtModelKeyBit, self).__init__()
        self.updated_at_field_name = updated_at_field_name

    def get_data(self, params, view_instance, view_method, request, args, kwargs):
        queryset = api_models.User.objects.filter(
            id=request.user.id,
        )
        user = queryset.only(self.updated_at_field_name).first()
        if not user:
            return None

        return force_text(user.updated_at)


class CurrentUserRetrieveKeyConstructor(KeyConstructor):
    user = bits.UserKeyBit()
    updated_at = UpdatedAtModelKeyBit()
    format = bits.FormatKeyBit()
