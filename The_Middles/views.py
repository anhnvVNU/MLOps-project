from django.shortcuts import render
from store.models import Book

def home(request):
    books = Book.objects.all().filter()
    context = {
        'books': books,
    }
    return render(request, 'home.html', context=context)