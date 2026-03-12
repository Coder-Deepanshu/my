from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class LeavePagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'size'
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'results': data,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
        })

class LabPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'results': data,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
        })


from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class standardPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'
    max_page_size = 50

# Common Pagination
class CommonPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'
    max_page_size = 50
