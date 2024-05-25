from django.contrib import admin
from .models import Variation, ReviewRating, Book, Author, AuthorCredit

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'stock')
    list_filter = ('release_date',)
    search_fields = ('title',)
    date_hierarchy = 'release_date'
    prepopulated_fields = {'slug': ('title',)}

class AuthorCreditAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'author_name')  # Sử dụng các phương thức đã định nghĩa

    def book_title(self, obj):
        return obj.book.title
    book_title.short_description = 'Book Title'

    def author_name(self, obj):
        return obj.author.name
    author_name.short_description = 'Author Name'
    
admin.site.register(ReviewRating)
admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(AuthorCredit, AuthorCreditAdmin)
