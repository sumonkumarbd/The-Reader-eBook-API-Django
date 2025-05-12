from rest_framework import serializers
from .models import Book, Category, Language
from storage.supabase_storage import SupabaseStorage
from django.db import transaction
import mimetypes

class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    category = serializers.CharField()
    language = serializers.CharField()
    publisher = serializers.CharField(allow_blank=True, allow_null=True)
    pdf_file = serializers.FileField(write_only=True, required=False)
    cover_image = serializers.ImageField(write_only=True, required=False)
    pdf_url = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()
    upload_date = serializers.DateTimeField(read_only=True,format='%d-%m-%Y')
    publication_date = serializers.DateField(format='%d-%m-%Y', input_formats=['%d-%m-%Y'], required=False)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'slug', 'category', 'language', 
                 'publisher', 'publication_date', 'description', 
                 'pdf_file', 'cover_image', 'pdf_url', 'cover_url',
                 'upload_date', 'featured']
        read_only_fields = ['upload_date', 'user', 'pdf_url', 'cover_url']



    def get_pdf_url(self, obj):
        if obj.pdf_file:
            # Return the URL for the PDF file from Supabase
            # This might need to be adjusted based on your Supabase setup
            return f'{obj.pdf_file}'
        return None

    def get_cover_url(self, obj):
        if obj.cover_image:
            # Return the URL for the cover image from Supabase
            # This might need to be adjusted based on your Supabase setup
            return f'{obj.cover_image}'
        return None

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get('request')
        
        # Add user if available
        if hasattr(request, 'user'):
            validated_data['user'] = request.user

        # Store file objects and remove from validated_data
        pdf_file = validated_data.pop('pdf_file', None)
        cover_image = validated_data.pop('cover_image', None)

        # Resolve foreign keys
        category_name = validated_data.pop('category')
        language_name = validated_data.pop('language')
        
        try:
            category = Category.objects.get(name=category_name)
            language = Language.objects.get(name=language_name)
            
            # Create book with all other data first (without files)
            book = Book.objects.create(
                category=category,
                language=language,
                **validated_data
            )
            
            # Initialize Supabase storage
            storage = SupabaseStorage()
            
            # Handle PDF file
            if pdf_file:
                pdf_filename = f"eBooks/{book.id}_{pdf_file.name}"
                mime_type, _ = mimetypes.guess_type(pdf_filename.name)
                content_type = mime_type or "application/octet-stream"
                # Upload file to Supabase and get the path
                pdf_path = storage.save(pdf_filename, pdf_file, content_type)
                # Set the file path in the model
                book.pdf_file = pdf_path
            
            # Handle cover image
            if cover_image:
                image_filename = f"images/{book.id}_{cover_image.name}"
                mime_type, _ = mimetypes.guess_type(image_filename.name)
                content_type = mime_type or "image/jpeg"
                # Upload file to Supabase and get the path
                image_path = storage.save(image_filename, cover_image)
                # Set the file path in the model
                book.cover_image = image_path
            
            # Save the model if files were added
            if pdf_file or cover_image:
                book.save()
                
            return book
            
        except Exception as e:
            # If any error occurs, the transaction will be rolled back
            # Files won't be saved to Supabase
            raise e

    @transaction.atomic
    def update(self, instance, validated_data):
        request = self.context.get('request')
        
        # Get and remove file objects from validated_data
        pdf_file = validated_data.pop('pdf_file', None)
        cover_image = validated_data.pop('cover_image', None)

        try:
            # Update foreign keys if provided
            if 'category' in validated_data:
                category_name = validated_data.pop('category')
                instance.category = Category.objects.get(name=category_name)

            if 'language' in validated_data:
                language_name = validated_data.pop('language')
                instance.language = Language.objects.get(name=language_name)

            # Update all other fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            
            # Save instance with updated non-file fields
            instance.save()
            
            # Initialize Supabase storage
            storage = SupabaseStorage()
            
            # Handle PDF file
            if pdf_file:
                pdf_filename = f"eBooks/{instance.id}_{pdf_file.name}"
                mime_type, _ = mimetypes.guess_type(pdf_filename.name)
                content_type = mime_type or "application/octet-stream"
                # Upload file to Supabase and get the path
                pdf_path = storage.save(pdf_filename, pdf_file, content_type)
                # Set the file path in the model
                instance.pdf_file = pdf_path
            
            # Handle cover image
            if cover_image:
                image_filename = f"images/{instance.id}_{cover_image.name}"
                mime_type, _ = mimetypes.guess_type(image_filename.name)
                content_type = mime_type or "image/jpeg"
                # Upload file to Supabase and get the path
                image_path = storage.save(image_filename, cover_image)
                # Set the file path in the model
                instance.cover_image = image_path
            
            # Save the instance again if files were updated
            if pdf_file or cover_image:
                instance.save()
                
            return instance
            
        except Exception as e:
            # If any error occurs, the transaction will be rolled back
            # Files won't be saved to Supabase
            raise e