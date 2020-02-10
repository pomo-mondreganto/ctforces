from collections import OrderedDict

import six
from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNumberWithPageSizePagination(PageNumberPagination):
    page_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_size', self.page_size),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        self.page_size = page_size

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)


class UserDefaultPagination(PageNumberWithPageSizePagination):
    page_size = 20
    max_page_size = 100


class TeamDefaultPagination(PageNumberWithPageSizePagination):
    page_size = 20
    max_page_size = 50


class ScoreboardPagination(PageNumberWithPageSizePagination):
    page_size = 20
    max_page_size = 100


class TaskDefaultPagination(PageNumberWithPageSizePagination):
    page_size = 30
    max_page_size = 50


class TaskFileDefaultPagination(PageNumberWithPageSizePagination):
    page_size = 30
    max_page_size = 50


class PostDefaultPagination(PageNumberWithPageSizePagination):
    page_size = 10
    max_page_size = 20


class ContestRegistrationsPagination(PageNumberWithPageSizePagination):
    page_size = 30
    max_page_size = 50


class ContestDefaultPagination(PageNumberWithPageSizePagination):
    page_size = 10
    max_page_size = 20


def get_paginated_data(paginator, queryset, serializer_class, request):
    page = paginator.paginate_queryset(
        queryset=queryset,
        request=request,
    )

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator, serializer.data

    serializer = serializer_class(queryset, many=True)
    return None, serializer.data


def get_paginated_response(paginator, queryset, serializer_class, request):
    page = paginator.paginate_queryset(
        queryset=queryset,
        request=request,
    )

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)
    return Response(serializer.data)
