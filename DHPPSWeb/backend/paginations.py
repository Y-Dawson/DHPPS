from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyFormatResultsSetPagination(PageNumberPagination):
    m_pageSizeQueryParam = "pageSize"
    m_pageQueryParam = 'page'
    m_pageSize = 6
    m_maxPageSize = 10

    """
    自定义分页方法
    """
    def GetPaginatedResponse(self, data):
        """
        设置返回内容格式
        """
        return Response({
            'data': data,
            'pagination': self.page.paginator.count,
            'pageSize': self.page.paginator.perPage,
            'page': self.page.startIndex() // self.page.paginator.perPage + 1
        })
