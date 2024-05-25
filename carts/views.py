from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from store.models import Book
from carts.models import Cart, CartItem


def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_cart(request, book_id):
    current_user = request.user
    book = Book.objects.get(id=book_id)    # Get object book
    if current_user.is_authenticated:
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST.get(key)

        is_exists_cart_item = CartItem.objects.filter(book=book, user=current_user).exists()
        if is_exists_cart_item:
            cart_items = CartItem.objects.filter(
                book=book,
                user=current_user
            )
            id = [item.id for item in cart_items]
        else:
            cart_item = CartItem.objects.create(
                book=book,
                user=current_user,
                quantity=1
            )
        return redirect('cart')
    else:
        return redirect('cart')


def remove_cart(request, book_id, cart_item_id):
    book = get_object_or_404(Book, id=book_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                id=cart_item_id,
                book=book,
                user=request.user
            )
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                id=cart_item_id,
                book=book,
                cart=cart
            )
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Exception:
        pass
    return redirect('cart')


def remove_cart_item(request, book_id, cart_item_id):
    Book = get_object_or_404(book, id=book_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                id=cart_item_id,
                book=book,
                user=request.user
            )
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request=request))
            cart_item = CartItem.objects.get(
                id=cart_item_id,
                book=book,
                cart=cart
            )
        cart_item.delete()
    except Exception:
        pass
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request=request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.book.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = total * 2 / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass    # Chỉ bỏ qua
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax if "tax" in locals() else "",
        'grand_total': grand_total if "tax" in locals() else 0,
    }
    return render(request, 'store/cart.html', context=context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        # cart = Cart.objects.get(cart_id=_cart_id(request=request))
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
            total += cart_item.book.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = total * 2 / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass    # Chỉ bỏ qua
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax if "tax" in locals() else "",
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context=context)