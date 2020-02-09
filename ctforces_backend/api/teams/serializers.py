from rest_framework import serializers as rest_serializers

from api import models as api_models
from api.mixins import ReadOnlySerializerMixin


class TeamMinimalSerializer(rest_serializers.ModelSerializer, ReadOnlySerializerMixin):
    rating = rest_serializers.IntegerField(read_only=True)

    class Meta:
        model = api_models.Team
        fields = (
            'id',
            'name',
            'rating',
        )
