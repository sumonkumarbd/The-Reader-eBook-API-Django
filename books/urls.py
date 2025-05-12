from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='home_page'),
    path('health_check', views.health_check),
    path('api/books/', views.getBooks, name='book-list-create'),
    path('api/books/<int:pk>/', views.bookDetail, name='book-detail'),
    path('ebooks/', views.see_eBooks, name='see_eBooks'),

]