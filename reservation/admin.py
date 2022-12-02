from django.contrib import admin

from reservation.models import BookInstance, ReservedBook

admin.site.register(BookInstance)
admin.site.register(ReservedBook)
