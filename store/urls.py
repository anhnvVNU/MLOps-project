from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='books_by_category'),
    path('search/', views.search, name='search'),
    path('sub_search/', views.sub_search, name='sub_search'),
    path('submit_review/<int:book_id>/', views.submit_review, name='submit_review'),
    path('submit_message/<int:book_id>/', views.submit_message, name='submit_message'),
    path('book/<slug:id>/', views.book_detail, name='book_detail'),
]