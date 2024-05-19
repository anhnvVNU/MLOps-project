from django.contrib import admin
from .models import Product, Variation, ReviewRating, Movie, Actor, CastCredit


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'created_date', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_date')
    list_editable = ('is_active',)   # Cho phép chỉnh sửa trên list hiển thị
    list_filter = ('product', 'variation_category', 'variation_value')

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'budget', 'release_date', 'popularity', 'vote_average')
    list_filter = ('release_date',)
    search_fields = ('title',)
    date_hierarchy = 'release_date'
    prepopulated_fields = {'homepage': ('title',)}

class CastCreditAdmin(admin.ModelAdmin):
    list_display = ('movie_title', 'actor_name','character_name','gender')  # Sử dụng các phương thức đã định nghĩa

    def movie_title(self, obj):
        return obj.movie.title
    movie_title.short_description = 'Movie Title'

    def actor_name(self, obj):
        return obj.actor.name
    actor_name.short_description = 'Actor Name'
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Actor)
admin.site.register(CastCredit, CastCreditAdmin)
