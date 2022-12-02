from django.core.management.base import BaseCommand
from django.db.models import Sum, Count, Avg
from django.db.models import IntegerField, Value

from books.models import Book
from djqscsv import write_csv


class Command(BaseCommand):
    help = 'Export books'

    def handle(self, *args, **options):
        books = Book.objects.all()\
            .annotate(
            borrowed_count=Count('book_instances__borrowed_book'),
            avg_score=Avg('book_review')
        ).values(
            'id',
            'title',
            'authors',
            'category__name',
            'publisher',
            'borrowed_count',
            'avg_score'
        )
        with open('export_library.csv', 'wb') as csv_file:
            write_csv(books, csv_file)
