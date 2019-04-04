from collections import OrderedDict

from guardian.shortcuts import get_objects_for_user
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPermissionsViewSetMixin:
    action_permission_classes = None

    def get_permissions(self):
        if self.action not in self.action_permission_classes:
            return super(CustomPermissionsViewSetMixin, self).get_permissions()
        return [permission() for permission in self.action_permission_classes[self.action]]


class CustomPermissionsQuerysetViewSetMixin:
    action_permissions_querysets = None
    klass = None

    def get_queryset(self):
        if self.action not in self.action_permissions_querysets:
            return super(CustomPermissionsQuerysetViewSetMixin, self).get_queryset()
        if not self.klass:
            raise AssertionError('Need to specify class to fetch permissions for (klass)')
        return get_objects_for_user(self.request.user, self.action_permissions_querysets[self.action], self.klass)


class PageNumberWithPageSizePagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_size', self.page_size),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class ReadOnlySerializerMixin:
    def create(self, *args, **kwargs):
        raise NotImplemented

    def update(self, *args, **kwargs):
        raise NotImplemented
