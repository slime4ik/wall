from rest_framework import serializers
from image.models import Wallpaper, Tag, Report

class ImagePreviewSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    thumbnail = serializers.SerializerMethodField()
    # tags = serializers.SerializerMethodField()
    total_likes = serializers.IntegerField()
    # liked_by_user = serializers.BooleanField()
    class Meta:
        model = Wallpaper
        fields = (
            'id',
            'creator',
            'title',
            'thumbnail',
            # 'type',
            # 'tags',
            'total_likes',
            'height',
            'width'
            # 'liked_by_user'
        )

    # def get_creator(self, obj):
    #     return str(obj.creator)

    def get_thumbnail(self, obj):
        if obj.thumbnail:
            try:
                return obj.thumbnail.url
            except Exception as e:
                print(f"Error getting thumbnail URL: {e}")
                return None
        elif obj.wallpaper:
            try:
                return obj.wallpaper.url
            except Exception as e:
                print(f"Error getting wallpaper URL: {e}")
                return None
        return None

    # def get_tags(self, obj):
    #     return [tag.name for tag in obj.tags.all()]
    

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

class WallpaperUploadSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

    class Meta:
        model = Wallpaper
        fields = ["title", "wallpaper", "type", "tags"]

    def validate_wallpaper(self, value):
        # Проверка расширения
        valid_extensions = ['.jpg', '.jpeg', '.png']
        if not any(str(value.name).lower().endswith(ext) for ext in valid_extensions):
            raise serializers.ValidationError("Incorrect file format.")
        # Проверка размера
        max_size = 5 * 1024 * 1024  # 5 MB
        if value.size > max_size:
            raise serializers.ValidationError("File is too big.")
        return value

    def validate_tags(self, value):
        if len(value) > 5:
            raise serializers.ValidationError("You can't add more than 5 tags")
        return value

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        wallpaper = Wallpaper.objects.create(**validated_data)
        wallpaper.tags.set(tags)
        return wallpaper

class WallpaperDetailSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    wallpaper = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    total_likes = serializers.IntegerField()
    liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Wallpaper
        fields = (
            'id',
            'creator',
            'title',
            'wallpaper',
            'type',
            'tags',
            'total_likes',
            'width',
            'height',
            'liked_by_user'
        )

    def get_creator(self, obj):
        return str(obj.creator)

    def get_wallpaper(self, obj):
        if obj.wallpaper:
            try:
                return obj.wallpaper.url
            except Exception as e:
                print(f"Error generating thumbnail URL: {e}")
        return None

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_liked_by_user(self, obj):
        return bool(getattr(obj, 'liked_by_user', False))

class ReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['target', 'message']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)