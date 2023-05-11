from rest_framework.pagination import PageNumberPagination


class LimitFieldPagination(PageNumberPagination):
    page_size_query_param = 'limit'
