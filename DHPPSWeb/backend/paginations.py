from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyFormatResultsSetPagination(PageNumberPagination):
    page_size_query_param = "pageSize"
    page_query_param = 'page'
    page_size = 6
    max_page_size = 10

    """
    自定义分页方法
    """
    def get_paginated_response(self, data):
        """
        设置返回内容格式
        """
        return Response({
            'data': data,
            'pagination': self.page.paginator.count,
            'pageSize': self.page.paginator.per_page,
            'page': self.page.start_index() // self.page.paginator.per_page + 1
        })
