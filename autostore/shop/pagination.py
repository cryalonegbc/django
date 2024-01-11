from rest_framework import pagination

class CarsPagination(pagination.PageNumberPagination):
    page_size = 6