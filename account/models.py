from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
from image.models import Wallpaper

class User(AbstractUser):
    pass

    def __str__(self) -> str:
        return self.username

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    wallpaper = models.ForeignKey(Wallpaper, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username} likes {self.wallpaper.title}'
    
    class Meta:
        unique_together = ('wallpaper', 'user')
        indexes = [
            models.Index(fields=['wallpaper', 'user']),
        ]
