from celery import shared_task
from PIL import Image
import io
from django.core.files.base import ContentFile
from image.models import Wallpaper

@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def save_thumbnail(wallpaper_id):
    """
    Быстро генерирует превью для обоев с сохранением пропорций
    """
    try:
        wallpaper = Wallpaper.objects.get(id=wallpaper_id)

        if not wallpaper.wallpaper:
            return f"Wallpaper {wallpaper_id} has no image."

        # Открываем изображение
        img = Image.open(wallpaper.wallpaper)
        
        # Сохраняем оригинальные размеры
        wallpaper.width, wallpaper.height = img.size
        wallpaper.save()

        # Быстрое создание превью с сохранением пропорций
        # Максимальный размер для превью
        max_thumb_size = (400, 400)
        
        # Создаем миниатюру с сохранением пропорций
        img.thumbnail(max_thumb_size, Image.Resampling.LANCZOS)
        
        # Конвертируем в RGB если нужно (для JPEG)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        # Сохраняем в буфер с быстрыми настройками
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=75, optimize=True)
        buffer.seek(0)

        # Имя файла для превью
        thumb_name = f"thumbnails/{wallpaper.id}_thumb.jpg"

        # Сохраняем миниатюру
        wallpaper.thumbnail.save(thumb_name, ContentFile(buffer.read()), save=True)

        return f"Thumbnail generated for wallpaper {wallpaper_id}"

    except Wallpaper.DoesNotExist:
        return f"Wallpaper {wallpaper_id} does not exist."
    except Exception as e:
        return f"Error generating thumbnail: {str(e)}"