from rest_framework import serializers
from .models import Book, Category, Language
from storage.supabase_storage import SupabaseStorage

class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    category = serializers.CharField()
    language = serializers.CharField()
    publisher = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['upload_date', 'user']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user

        # Resolve foreign keys
        category_name = validated_data.pop('category')
        language_name = validated_data.pop('language')
        category = Category.objects.get(name=category_name)
        language = Language.objects.get(name=language_name)

        # Manual file upload
        storage = SupabaseStorage()
        files = request.FILES

        if 'pdf_file' in files:
            file_obj = files['pdf_file']
            path = f"eBooks/{file_obj.name}"
            storage._save(path, file_obj)
            validated_data['pdf_file'] = path

        if 'cover_image' in files:
            image_obj = files['cover_image']
            path = f"images/{image_obj.name}"
            storage._save(path, image_obj)
            validated_data['cover_image'] = path

        book = Book.objects.create(
            category=category,
            language=language,
            **validated_data
        )
        return book

    def update(self, instance, validated_data):
        request = self.context.get('request')
        storage = SupabaseStorage()
        files = request.FILES

        if 'category' in validated_data:
            category_name = validated_data.pop('category')
            instance.category = Category.objects.get(name=category_name)

        if 'language' in validated_data:
            language_name = validated_data.pop('language')
            instance.language = Language.objects.get(name=language_name)

        if 'pdf_file' in files:
            file_obj = files['pdf_file']
            path = f"eBooks/{file_obj.name}"
            storage._save(path, file_obj)
            instance.pdf_file = path

        if 'cover_image' in files:
            image_obj = files['cover_image']
            path = f"images/{image_obj.name}"
            storage._save(path, image_obj)
            instance.cover_image = path

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
