from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('danh-muc-san-pham/', views.category, name='category'),
    path('danh-muc-san-pham/<type>', views.category, name='category'),
]
