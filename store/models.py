
from django.urls import reverse
from category.models import Category
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
    
    
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    image_urls = models.URLField(max_length=200, blank=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)    # Khi xóa category thì Product bị xóa
    release_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('book_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.title

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=200, unique=True, default="n/a")
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=30, default="N/A1", blank=True)
    GENDER_CHOICES = (
        (0, 'Not specified'),
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other'),
    )
    
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0)

    def __str__(self):
        return self.name


class AuthorCredit(models.Model):
    # id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=1)   # Khi xóa book thì AuthorCredit bị xóa
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=1)   # Khi xóa author thì AuthorCredit bị xóa

    def __str__(self):
        return f"{self.character_name} in {self.book.title} played by {self.author.name}"


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=1)
    slug = models.SlugField(max_length=200, unique=True, default="n/a")
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class ReviewBookRating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)