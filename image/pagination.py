from rest_framework.pagination import PageNumberPagination

class WallpaperPreviewPagination(PageNumberPagination):
    """15 wallpapers per page"""
    page_size = 15
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 15

class BestWallpaperPreviewPagination(PageNumberPagination):
    """15 wallpapers per page"""
    page_size = 15
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 15