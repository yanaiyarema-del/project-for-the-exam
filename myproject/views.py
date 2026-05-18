from django.shortcuts import render
from books.models import Book
from django.contrib import messages

def home_view(request):
    books = Book.objects.all().order_by('-id')[:12]
    return render(request, 'home.html', {'books': books})