from django.shortcuts import get_object_or_404
from rest_framework import serializers
from borrow.models import BorrowedBook, BookInstance
from django.core.exceptions import ObjectDoesNotExist


class BorrowBookSerializer(serializers.Serializer):
    book = serializers.IntegerField(required=True)

    def validate_book(self, value):
        get_object_or_404(BookInstance, pk=value)
        return value

    def validate(self, data):
        try:
            BorrowedBook.objects.get(book_id=data.get('book'), user=self.context.get("request").user)
            raise serializers.ValidationError("You've already borrowed this book")
        except ObjectDoesNotExist:
            pass
        borrowed_count = BorrowedBook.objects.filter(
            user_id=self.context.get("request").user,
            returned_at__isnull=True
        ).count()
        if borrowed_count >= 3:
            raise serializers.ValidationError("You can't borrow more than 3 book at the same time")
        return data
