import django_filters
from .models import Wallpaper, Tag

class WallpapersFilterBackend(django_filters.FilterSet):
    """Search"""
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags",
        queryset=Tag.objects.all()
    )
    class Meta:
        model = Wallpaper
        fields = ["title", "tags", "type"]
