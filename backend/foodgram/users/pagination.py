from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    """Custom pagination class."""
    page_size = 2
    page_size_query_param = 'limit'
