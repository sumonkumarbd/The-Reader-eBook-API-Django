from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Book
from storage.supabase_storage import SupabaseStorage
import logging

logger = logging.getLogger(__name__)

@receiver(post_delete, sender=Book)
def delete_related_files(sender, instance, **kwargs):
    # Get your file URLs (implement these methods as you need)
    pdf_url = instance.pdf_file.url if instance.pdf_file else None
    cover_url = instance.cover_image.url if instance.cover_image else None
    pdf_path = pdf_url.split('/the-reader-ebook/')[-1]
    image_path = cover_url.split('/the-reader-ebook/')[-1]
    paths = []
    if instance.pdf_file:
        paths.append(pdf_path)
    if instance.cover_image:
        paths.append(image_path)
    if paths:
        try:
            storage = SupabaseStorage()
            result = storage.delete(paths)
            logger.info(f"Deleted files: {paths}, result: {result}")
        except Exception as e:
            logger.error(f"Error deleting files from Supabase: {e}")