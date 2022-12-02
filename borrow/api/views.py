from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrow.models import BorrowedBook, BookInstance
from .serializers import BorrowBookSerializer


class BorrowBookView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        context = {'request': self.request}
        serializer = BorrowBookSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        BorrowedBook.objects.create(
            book_id=data.pop('book'),
            user=self.request.user
        )
        return Response(status=status.HTTP_200_OK)