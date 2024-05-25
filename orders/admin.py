from django.contrib import admin
from .models import Order, OrderBook, Payment


admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(OrderBook)