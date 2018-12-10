from guardian.shortcuts import assign_perm
from rest_framework import serializers as rest_serializers

from api import models as api_models


class PostMainSerializer(rest_serializers.ModelSerializer):
    can_edit_post = rest_serializers.BooleanField(required=False, read_only=True)

    class Meta:
        model = api_models.Post
        fields = (
            'id',
            'author',
            'body',
            'can_edit_post',
            'created_at',
            'is_published',
            'title',
            'updated_at',
        )

        extra_kwargs = {
            'created_at': {
                'read_only': True,
            },
            'updated_at': {
                'read_only': True,
            },
        }

    def validate(self, attrs):
        attrs['author'] = self.context['request'].user
        return attrs

    def create(self, validated_data):
        instance = super(PostMainSerializer, self).create(validated_data)
        assign_perm('view_post', instance.author, instance)
        assign_perm('change_post', instance.author, instance)
        return instance
