from django.contrib import admin

from books.models import Book, BookCategory, BookReview

admin.site.register(Book)
admin.site.register(BookCategory)
admin.site.register(BookReview)
