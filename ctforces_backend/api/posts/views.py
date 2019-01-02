from rest_framework import mixins as rest_mixins
from rest_framework import viewsets as rest_viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api import mixins as api_mixins
from api import models as api_models
from api import pagination as api_pagination
from api import permissions as api_permissions
from api.posts import serializers as api_posts_serializers


class PostViewSet(api_mixins.CustomPermissionsViewSetMixin,
                  api_mixins.CustomPermissionsQuerysetViewSetMixin,
                  rest_mixins.RetrieveModelMixin,
                  rest_mixins.ListModelMixin,
                  rest_mixins.CreateModelMixin,
                  rest_mixins.UpdateModelMixin,
                  rest_viewsets.GenericViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, api_permissions.HasEditPostPermissionOrReadOnly)
    pagination_class = api_pagination.PostDefaultPagination
    serializer_class = api_posts_serializers.PostMainSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = api_models.Post.objects.all()

    def get_queryset(self):
        qs = super(PostViewSet, self).get_queryset()
        if self.action == 'list':
            return qs.filter(show_on_main_page=True)
        return qs

    klass = api_models.Post
    action_permissions_querysets = {
        'update': 'change_post',
        'partial_update': 'change_post',
    }

    action_permission_classes = {
        'retrieve': api_permissions.HasViewPostPermission,
    }

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.can_edit_post = request.user.has_perm('change_post')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
