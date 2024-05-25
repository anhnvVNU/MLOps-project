from orders.models import OrderBook
from django.contrib import messages
from store.forms import ReviewForm
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.db.models import Q

from store.models import ReviewRating, Book, ReviewBookRating
from carts.models import Cart, CartItem
from category.models import Category
from carts.views import _cart_id

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .chatModel import response_AI
from datetime import datetime

def store(request, category_slug=None):
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        books = Book.objects.all().filter(genres=categories)
    else:
        books = Book.objects.all().order_by('id')

    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(books, 3)
    paged_books = paginator.get_page(page)
    book_count = books.count()

    context = {
        'books': paged_books,
        'book_count': book_count,
        "slug": False
    }
    return render(request, 'store/store.html', context=context)


def book_detail(request, id):
    try:
        single_book = Book.objects.get(id=id)
        print(single_book)
        cart = Cart.objects.get(cart_id=_cart_id(request=request))
        in_cart = CartItem.objects.filter(
            cart=cart,
            book=single_book
        ).exists()
    except Exception as e:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )

    try:
        orderbook = OrderBook.objects.filter(user=request.user, book_id=single_book.id).exists()
    except Exception:
        orderbook = None

    reviews = ReviewRating.objects.filter(book_id=single_book.id)

    ratings = ["5", "4.5", "4", "3.5", "3", "2.5", "2", "1.5", "1", "0.5"]

    context = {
        'single_book': single_book,
        'in_cart': in_cart if 'in_cart' in locals() else False,
        'orderbook': orderbook,
        'reviews': reviews,
        'ratings': ratings
    }
    return render(request, 'store/book_detail.html', context=context)

def search(request):
    if 'q' in request.GET:
        q = request.GET.get('q')
        books = Book.objects.order_by('-release_date').filter(Q(title__icontains=q) | Q(overview__icontains=q))
        book_count = books.count()
    context = {
        'books': books,
        'q': q,
        'book_count': book_count,
        "slug": True
    }
    return render(request, 'store/store.html', context=context)


def sub_search(request):
    genre_ids = request.GET.getlist('genre')
    min_rating = float(request.GET.get('min_rating', 1))
    max_rating = float(request.GET.get('max_rating', 5))
    min_price = float(request.GET.get('min_price', 0))
    max_price = float(request.GET.get('max_price', 100000))
    release_date_min_str = request.GET.get('release_date_min', "")
    release_date_max_str = request.GET.get('release_date_max', "")
    author_name = request.GET.get('author', '')

    genre_ids = [int(genre_id) for genre_id in genre_ids]

    release_date_min = datetime.strptime(release_date_min_str, '%Y-%m-%d') if release_date_min_str else None
    release_date_max = datetime.strptime(release_date_max_str, '%Y-%m-%d') if release_date_max_str else datetime.now()

    # Start with all books and then apply filters
    books = Book.objects.all()

    if genre_ids:
        books = Books.filter(genres__id__in=genre_ids)

    if min_rating or max_rating:
        books = Books.filter(vote_average__gte=min_rating, vote_average__lte=max_rating)

    if min_price or max_price:
        books = Books.filter(price__gte=min_price, price__lte=max_price)


    if release_date_min:
        books = Books.filter(release_date__gte=release_date_min, release_date__lte=release_date_max)
    else:
        books = Books.filter(release_date__lte=release_date_max)


    if author_name:
        # Lấy danh sách các bộ phim mà diễn viên đó tham gia
        books = Books.filter(authorcredit__author__name__icontains=author_name)
    book_count = books.count()
    context = {
        'books': books,
        'book_count': book_count,
        "author": author_name,
        "genre_ids": genre_ids,
        "min_rating": min_rating,
        "max_rating": max_rating,
        "min_price": min_price,
        "max_price": max_price,
        "release_date_min": release_date_min_str,
        "release_date_max": release_date_max_str,
        "slug": True
    }

    print(context)

    return render(request, 'store/store.html', context=context)



def submit_review(request, book_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            review = ReviewRating.objects.get(user__id=request.user.id, book__id=book_id)
            form = ReviewForm(request.POST, instance=review)
            form.save()
            messages.success(request, "Thank you! Your review has been updated.")
            return redirect(url)
        except Exception:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.book_id = book_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted.")
                return redirect(url)

@csrf_exempt
def submit_message(request, book_id):
    if request.method == "POST":
        try:
            # Lưu tin nhắn vào cơ sở dữ liệu hoặc thực hiện các thao tác cần thiết
            message = request.POST.get('message', None)
            # Do something with the message
            response = response_AI(message= message)
            return JsonResponse({'success': True, 'message' : response})  # Trả về một phản hồi JSON thành công
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})  # Trả về một phản hồi JSON lỗi nếu có lỗi xảy ra
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})  # Trả về một phản hồi JSON lỗi nếu yêu cầu không hợp lệ