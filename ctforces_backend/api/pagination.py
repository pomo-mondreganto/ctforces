from rest_framework.pagination import PageNumberPagination


class UserTopPagination(PageNumberPagination):
    page_size = 50
    max_page_size = 100
    page_size_query_param = 'page_size'
