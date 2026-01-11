from rest_framework.pagination import PageNumberPagination

class LeavePagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = None
    max_page_size = 50