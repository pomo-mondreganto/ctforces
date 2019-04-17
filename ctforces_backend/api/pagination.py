from rest_framework.response import Response

from api.mixins import PageNumberWithPageSizePagination


class UserDefaultPagination(PageNumberWithPageSizePagination):
    page_size = 20
    max_page_size = 100
    page_size_query_param = 'page_size'


class UserScoreboardPagination(PageNumberWithPageSizePagination):
    page_size = 20
    max_page_size = 100
    page_size_query_param = 'page_size'


class TaskDefaultPagination(PageNumberWithPageSizePagination):
    page_size = 30
    max_page_size = 50
    page_size_query_param = 'page_size'


class TaskFileDefaultPagination(PageNumberWithPageSizePagination):
    page_size = 30
    max_page_size = 50
    page_size_query_param = 'page_size'


class PostDefaultPagination(PageNumberWithPageSizePagination):
    page_size = 10
    max_page_size = 20
    page_size_query_param = 'page_size'


class ContestDefaultPagination(PageNumberWithPageSizePagination):
    page_size = 10
    max_page_size = 20
    page_size_query_param = 'page_size'


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
