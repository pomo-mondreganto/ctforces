from api.mixins import PageNumberWithPageSizePagination


class UserDefaultPagination(PageNumberWithPageSizePagination):
    page_size = 50
    max_page_size = 100
    page_size_query_param = 'page_size'


class UserScoreboardPagination(PageNumberWithPageSizePagination):
    page_size = 20
    max_page_size = 20
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
