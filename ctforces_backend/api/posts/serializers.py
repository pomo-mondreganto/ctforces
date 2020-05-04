from guardian.shortcuts import assign_perm
from rest_framework import serializers as rest_serializers

from api import models as api_models


class PostMainSerializer(rest_serializers.ModelSerializer):
    author = rest_serializers.HiddenField(default=rest_serializers.CurrentUserDefault())
    can_edit_post = rest_serializers.BooleanField(required=False, read_only=True)
    author_username = rest_serializers.SlugRelatedField(read_only=True, slug_field='username', source='author')
    author_rating = rest_serializers.SlugRelatedField(read_only=True, slug_field='rating', source='author')

    class Meta:
        model = api_models.Post
        fields = (
            'author',
            'author_rating',
            'author_username',
            'body',
            'can_edit_post',
            'created_at',
            'id',
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

    def create(self, validated_data):
        instance = super(PostMainSerializer, self).create(validated_data)
        assign_perm('view_post', instance.author, instance)
        assign_perm('change_post', instance.author, instance)
        return instance
