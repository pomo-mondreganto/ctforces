from rest_framework import mixins as rest_mixins
from rest_framework import viewsets as rest_viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response

import api.mixins
import api.models
import api.pagination
import api.posts.caching
import api.posts.permissions
import api.posts.serializers


class PostViewSet(api.mixins.CustomPermissionsViewSetMixin,
                  rest_mixins.RetrieveModelMixin,
                  rest_mixins.ListModelMixin,
                  rest_mixins.CreateModelMixin,
                  rest_mixins.UpdateModelMixin,
                  rest_viewsets.GenericViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = api.pagination.PostDefaultPagination
    serializer_class = api.posts.serializers.PostMainSerializer
    queryset = api.models.Post.objects.all().select_related('author')

    def get_queryset(self):
        qs = super(PostViewSet, self).get_queryset()
        if self.action == 'list':
            return qs.filter(show_on_main_page=True)
        return qs

    action_permission_classes = {
        'retrieve': (api.posts.permissions.HasViewPostPermission,),
        'update': (api.posts.permissions.HasEditPostPermission,),
        'partial_update': (api.posts.permissions.HasEditPostPermission,),
    }

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.can_edit_post = request.user.has_perm('change_post', instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @cache_response(timeout=60, key_func=api.posts.caching.PostListKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super(PostViewSet, self).list(request, *args, **kwargs)
