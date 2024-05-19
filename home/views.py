from django.shortcuts import render
from .models import Product

def home(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'homepage.html', context=context)

def category(request, type):
    if type == 'tat-ca':
        products = Product.objects.all()
        category_name = "Tất cả danh mục"
    elif type == 'dien-tu':
        products = Product.objects.filter(category_type='Điện tử')
        category_name = "Danh mục Điện tử"
    elif type == 'sach':
        products = Product.objects.filter(category_type='Sách')
        category_name = "Danh mục Sách"
    elif type == 'mon-an':
        products = Product.objects.filter(category_type='Món ăn')
        category_name = "Danh mục Món ăn"
    elif type == 've-phim':
        products = Product.objects.filter(category_type='Vé phim')
        category_name = "Danh mục Vé phim"
    elif type == 'quan-ao':
        products = Product.objects.filter(category_type='Quần áo')
        category_name = "Danh mục Quần áo"
    elif type == 'meo':
        products = Product.objects.filter(category_type='Meo~~')
        category_name = "Danh mục Meo~~"

    context = {
        'products': products,
        'category_name': category_name,
    }
    return render(request, 'category.html', context=context)
