from django.contrib import admin
from django.db.models import Q
from .models import *




class BookAdmin(admin.ModelAdmin):
    exclude = ('user',)
    list_display = ('title', 'author', 'category', 'upload_date', 'featured')
    list_filter = ('author', 'category', 'upload_date', 'featured')
    prepopulated_fields = {'slug':('title','author')}
    search_fields = ('title','description','author')
    actions = ('set_book_to_featured','set_book_to_unfeatured')
    # fields = (('title', 'author'),'category', 'featured','slug')

    def get_search_results(self, request, queryset, search_term):
        queryset = queryset.filter(Q(title__icontains=search_term) | Q(description__icontains=search_term) | Q(author__icontains=search_term))
        return queryset, False
    

    def set_book_to_featured(self,request,queryset):
        count = queryset.update(featured = True)
        self.message_user(request,'{} books have been featured'.format(count))
    set_book_to_featured.short_description = 'Mark selected books as featured'

    def set_book_to_unfeatured(self,request,queryset):
        count = queryset.update(featured = False)
        self.message_user(request,'{} books have been unfeatured'.format(count))
    set_book_to_unfeatured.short_description = 'Mark selected books as unfeatured'



# Register your models here.
admin.site.register(Category)
admin.site.register(Language)
admin.site.register(Book,BookAdmin)
