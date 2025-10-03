DEFAULT_TAGS = [
    "nature",
    "anime", 
    "art",
    "abstract",
    "minimal",
    "landscape",
    "city",
    "space",
    "fantasy",
    "game",
    "movie",
    "car",
    "animal",
    "flower",
    "sunset",
    "beach",
    "mountain",
    "forest",
    "water",
    "sky",
    "dark",
    "light",
    "colorful",
    "black",
    "white",
    "vintage",
    "modern",
    "cute",
    "cool",
    "aesthetic"
]

from django.core.management.base import BaseCommand
from image.models import Tag

class Command(BaseCommand):
    help = 'Create default tags'

    def handle(self, *args, **options):
        tags = [
            "nature", "anime", "art", "abstract", "minimal", 
            "landscape", "city", "space", "fantasy", "game",
            "movie", "car", "animal", "flower", "sunset",
            "beach", "mountain", "forest", "water", "sky",
            "dark", "light", "colorful", "black", "white",
            "vintage", "modern", "cute", "cool", "aesthetic"
        ]
        
        created_count = 0
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created tag: {tag_name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} tags')
        )