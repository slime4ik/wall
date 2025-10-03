from django.urls import path
from .views import WallpaperPreviewListAPIView, WallpaperCreateAPIView, TagsListAPIView, WallpaperLikeAPIView, WallpaperDetailAPIView,\
WallpaperSearchListAPIView, ReportCreateAPIView, WallpaperBookmarksListAPIView


urlpatterns = [
    path('best-wallpapers/', WallpaperPreviewListAPIView.as_view(), name='best-wallpapers'),
    path('create/', WallpaperCreateAPIView.as_view(), name='create'),
    path('tags/', TagsListAPIView.as_view(), name='tags'),
    path('wallpapers/<int:wallpaper_id>/like/', WallpaperLikeAPIView.as_view(), name='like'),
    path('wallpapers/<int:wallpaper_id>/', WallpaperDetailAPIView.as_view(), name='like'),
    path('wallpapers/', WallpaperSearchListAPIView.as_view(), name='wallpapers'),
    path('reports/', ReportCreateAPIView.as_view(), name='report-create'),
    path('bookmarks/', WallpaperBookmarksListAPIView.as_view(), name='bookmarks'),
]
