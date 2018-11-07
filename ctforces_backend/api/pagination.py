from rest_framework.pagination import PageNumberPagination


class UserDefaultPagination(PageNumberPagination):
    page_size = 50
    max_page_size = 100
    page_size_query_param = 'page_size'


class UserScoreboardPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20
    page_size_query_param = 'page_size'


class TaskDefaultPagination(PageNumberPagination):
    page_size = 30
    max_page_size = 50
    page_size_query_param = 'page_size'


class TaskFileDefaultPagination(PageNumberPagination):
    page_size = 30
    max_page_size = 50
    page_size_query_param = 'page_size'


class PostDefaultPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 20
    page_size_query_param = 'page_size'


class ContestDefaultPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 20
    page_size_query_param = 'page_size'
