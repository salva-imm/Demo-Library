from datetime import timedelta, date

from django.contrib.auth.models import User
from django.db import models
from django.db.models import DO_NOTHING
from django.utils.timezone import now

from books.models import Book


class BookInstance(models.Model):
    book = models.ForeignKey(Book, related_name='book_instances', on_delete=DO_NOTHING)
    amval_code = models.IntegerField(unique=True)


class BorrowedBook(models.Model):
    book = models.ForeignKey(BookInstance, related_name='borrowed_book', on_delete=DO_NOTHING)
    user = models.ForeignKey(User, on_delete=DO_NOTHING)
    created_at = models.DateTimeField(default=now)
    reserved_for_days = models.IntegerField(default=7)
    returned_at = models.DateTimeField(null=True, blank=True)

    @property
    def return_date(self) -> date:
        return (self.created_at + timedelta(days=self.reserved_for_days)).date()
