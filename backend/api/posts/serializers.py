from guardian.shortcuts import assign_perm
from rest_framework import serializers

from api.models import Post


class PostMainSerializer(serializers.ModelSerializer):
    can_edit_post = serializers.BooleanField(read_only=True)
    author_username = serializers.SlugRelatedField(read_only=True, slug_field='username', source='author')
    author_rating = serializers.SlugRelatedField(read_only=True, slug_field='rating', source='author')

    class Meta:
        model = Post
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
        validated_data['author'] = self.context['request'].user
        instance = super(PostMainSerializer, self).create(validated_data)
        assign_perm('view_post', instance.author, instance)
        assign_perm('change_post', instance.author, instance)
        return instance
