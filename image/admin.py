from django.contrib import admin
from django.utils.html import format_html
from .models import Wallpaper, WallpaperLike, Tag, Report
from django.contrib.admin import SimpleListFilter, RelatedOnlyFieldListFilter


# Wallpaper Admin
@admin.register(Wallpaper)
class WallpaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'type', 'is_active', 'thumbnail_preview', 'total_likes')
    list_filter = ('type', 'is_active', 'created_at')
    search_fields = ('title', 'creator__username', 'tags__name')
    readonly_fields = ('thumbnail_preview',)
    ordering = ('-created_at',)

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="100" />', obj.thumbnail.url)
        return "-"
    thumbnail_preview.short_description = "Thumbnail Preview"

    def total_likes(self, obj):
        return obj.likes.count()
    total_likes.short_description = "Likes"

# WallpaperLike Admin
@admin.register(WallpaperLike)
class WallpaperLikeAdmin(admin.ModelAdmin):
    list_display = ('wallpaper', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'wallpaper__title')
    ordering = ('-created_at',)

# Tag Admin
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "target", "message", "created_at", "wallpaper_type", "wallpaper_is_active")
    list_filter = ("created_at", "target__is_active")
    search_fields = ("message", "sender__username", "target__title")
    ordering = ("-created_at",)

    actions = ["deactivate_wallpaper", "delete_reports"]

    def wallpaper_type(self, obj):
        return obj.target.type
    wallpaper_type.short_description = "Type"

    def wallpaper_is_active(self, obj):
        return obj.target.is_active
    wallpaper_is_active.boolean = True
    wallpaper_is_active.short_description = "Active"

    @admin.action(description="Set wallpapers as unactive (is_active=False)")
    def deactivate_wallpaper(self, request, queryset):
        count = 0
        for report in queryset:
            wallpaper = report.target
            if wallpaper.is_active:
                wallpaper.is_active = False
                wallpaper.save()
                count += 1
        self.message_user(request, f"{count} wallpapers marked as unactive.")

    @admin.action(description="Delete choosen reports")
    def delete_reports(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} репортов удалено.")
