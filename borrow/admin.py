from django.contrib import admin

from borrow.models import BookInstance, BorrowedBook

admin.site.register(BookInstance)
admin.site.register(BorrowedBook)
