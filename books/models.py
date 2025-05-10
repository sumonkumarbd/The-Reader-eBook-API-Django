from django.db import models
from django.core.exceptions import ValidationError
import io

# Create your models here.
# Define Language model
class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Define Category model
class Category(models.Model):
    name = models.CharField(max_length=100)
    descriptions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# For validate PDF
def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')

# imagevalidator
def imagevalidator(value):
    if not value.name.endswith(('.png', '.jpg', '.jpeg')):
        raise ValidationError('Only PNG, JPG, and JPEG files are allowed.')

# Define Book model
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)  # Now Author is defined
    slug = models.SlugField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)  # Now Language is defined
    publisher = models.CharField(max_length=100 ,blank=True, null=True)  # Now Publisher is defined
    publication_date = models.DateField(blank=True, null=True)
    description = models.TextField()
    pdf_file = models.FileField(upload_to='storage/pdfs/', validators=[validate_pdf])
    cover_image = models.ImageField(upload_to='storage/covers/', validators=[imagevalidator])
    upload_date = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

