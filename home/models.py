from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    category_type = models.CharField(max_length=200, null=True, blank=True)
