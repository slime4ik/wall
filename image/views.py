from .serializers import ImagePreviewSerializer, ReportCreateSerializer, \
    WallpaperUploadSerializer, TagSerializer, WallpaperDetailSerializer
from rest_framework import generics
from .models import Report, Wallpaper, Tag, WallpaperLike
from .pagination import WallpaperPreviewPagination, BestWallpaperPreviewPagination
from rest_framework.views import APIView
from .tasks import save_thumbnail
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from .filters import WallpapersFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from supermaster.decorators import ratelimit # custom ratelimit returns 429
from django.utils.decorators import method_decorator


@method_decorator(ratelimit(key='ip', rate='80/m', method='GET'), name='get')
class WallpaperPreviewListAPIView(generics.ListAPIView):
    """Returns a list of 20 best Wallpapers"""
    serializer_class = ImagePreviewSerializer
    pagination_class = BestWallpaperPreviewPagination

    def get_queryset(self):
        return Wallpaper.objects.select_related("creator").\
                                    annotate(
                                        total_likes=Count('likes'),
                                    ).\
                                    filter(is_active=True).\
                                    order_by('-total_likes')

@method_decorator(ratelimit(key='ip', rate='80/m', method='GET'), name='get')
class WallpaperSearchListAPIView(generics.ListAPIView):
    """Returns a list of Wallpapers by user's query"""
    serializer_class = ImagePreviewSerializer
    pagination_class = WallpaperPreviewPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_class = WallpapersFilterBackend
    search_fields = ['title']
    filterset_fields = ['type', 'tags']
    def get_queryset(self):
        return Wallpaper.objects.select_related("creator").\
                                    annotate(
                                        total_likes=Count('likes'),
                                    ).\
                                    filter(is_active=True).\
                                    order_by('-total_likes')


@method_decorator(ratelimit(key='ip', rate='5/m', method='POST'), name='post')
class WallpaperCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = WallpaperUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Save wallpaper with creator
        wallpaper = serializer.save(creator=request.user)
        # Call async image processing
        save_thumbnail.delay(wallpaper.id)
        return Response(
            {"message": "Wallpaper successfully saved, generating thumbnail..."},
            status=status.HTTP_201_CREATED
        )

@method_decorator(ratelimit(key='ip', rate='50/m', method='GET'), name='get')
class TagsListAPIView(APIView):
    def get(self, request):
        tags = Tag.objects.all().order_by("name")  # by alphabet
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@method_decorator(ratelimit(key='ip', rate='90/m', method='POST'), name='post')
class WallpaperLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, wallpaper_id):
        wallpaper = Wallpaper.objects.get(id=wallpaper_id)
        like, created = WallpaperLike.objects.get_or_create(
            wallpaper=wallpaper, user=request.user
        )
        if not created:
            like.delete()
            return Response({"liked": False}, status=status.HTTP_201_CREATED)
        return Response({"liked": True}, status=status.HTTP_201_CREATED)

@method_decorator(ratelimit(key='ip', rate='70/m', method='GET'), name='get')
class WallpaperDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, wallpaper_id):
        wallpaper = get_object_or_404(
            Wallpaper.objects.select_related("creator")
                             .prefetch_related("tags")
                             .annotate(
                                 total_likes=Count('likes'),
                                 liked_by_user=Count('likes', filter=Q(likes__user=request.user))
                             ),
            id=wallpaper_id
        )
        serializer = WallpaperDetailSerializer(wallpaper)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@method_decorator(ratelimit(key='ip', rate='10/m', method='POST'), name='post')
class ReportCreateAPIView(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


@method_decorator(ratelimit(key='ip', rate='80/m', method='GET'), name='get')
class WallpaperBookmarksListAPIView(generics.ListAPIView):
    """Returns a list of user's bookmarked wallpapers"""
    serializer_class = ImagePreviewSerializer
    pagination_class = BestWallpaperPreviewPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wallpaper.objects.select_related("creator").\
                                    annotate(
                                        total_likes=Count('likes'),
                                    ).\
                                    filter(is_active=True, bookmark__user=self.request.user).\
                                    distinct().\
                                    order_by('-created_at')