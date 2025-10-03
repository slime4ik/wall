from django.db import models
from django.conf import settings

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Wallpaper(models.Model):
    TYPE_CHOICES = [
        ('PC', 'Компьютер'),
        ('PHONE', 'Телефон')
    ]
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='wallpapers')
    title = models.CharField(max_length=50)
    wallpaper = models.ImageField(upload_to='wallpapers/%Y/%m/%d/')
    thumbnail = models.ImageField(upload_to='thumbnails/%Y/%m/%d/')
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="wallpapers")
    type = models.CharField(choices=TYPE_CHOICES, max_length=5, default='PC')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['created_at', 'title']),
        ]

class WallpaperLike(models.Model):
    wallpaper = models.ForeignKey(Wallpaper, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('wallpaper', 'user')
        indexes = [
            models.Index(fields=['wallpaper', 'user']),
        ]

class Report(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    target = models.ForeignKey(Wallpaper, on_delete=models.CASCADE, related_name='reports')
    message = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)