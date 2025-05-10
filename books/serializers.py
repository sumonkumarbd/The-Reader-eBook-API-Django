from rest_framework import serializers
from .models import *

class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    category = serializers.CharField()
    language = serializers.CharField()
    publisher = serializers.CharField()

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['upload_date',]

    def create(self, validated_data):
        category_name = validated_data.pop('category')
        language_name = validated_data.pop('language')
    

        category = Category.objects.get(name=category_name)
        language = Language.objects.get(name=language_name)

        book = Book.objects.create(
            category=category,
            language=language,
            **validated_data
        )
        return book

    def update(self, instance, validated_data):
        if 'category' in validated_data:
            category_name = validated_data.pop('category')
            instance.category = Category.objects.get(name=category_name)

        if 'language' in validated_data:
            language_name = validated_data.pop('language')
            instance.language = Language.objects.get(name=language_name)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
