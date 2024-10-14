from rest_framework import pagination

from django.conf import settings


class PageNumberPagination(pagination.PageNumberPagination):
    page_size = settings.DEFAULT_PAGE_SIZE
    max_page_size = max(page_size, 100) if page_size else None
    page_query_param = "page"
    page_size_query_param = "per_page"


class DefaultPageNumberPagination(PageNumberPagination):
    page_size = 6


class SmallPageNumberPagination(PageNumberPagination):
    page_size = 2
