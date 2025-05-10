from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from .serializers import *
import os

# Create your views here.
def health_check(request):
    return JsonResponse({"message": "API is working!"})

def index(request):
    books = Book.objects.all()
    return render(request, 'index.html', {'books': books})

@api_view(['GET', 'POST'])
def getBooks(request):
    #get
    if request.method == 'GET':
        all_books = Book.objects.all()
        serializer = BookSerializer(all_books, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #post
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #root
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def bookDetail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'error':'Book not found!'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    elif request.method in ['PUT','PATCH']:
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        book.delete()
        return Response({'message': 'Book deleted'}, status=status.HTTP_204_NO_CONTENT)

def download_pdf(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        # For Vercel deployment, redirect to the file URL instead of serving directly
        if book.pdf_file:
            return HttpResponseRedirect(book.pdf_file.url)
        return HttpResponse("PDF not found", status=404)
    except Book.DoesNotExist:
        return HttpResponse("Book not found", status=404)

def download_cover(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        if book.cover_image:
            return HttpResponseRedirect(book.cover_image.url)
        return HttpResponse("Cover image not available", status=404)
    except Book.DoesNotExist:
        return HttpResponse("Book not found", status=404)