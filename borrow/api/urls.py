from django.urls import path
from .views import BorrowBookView

app_name = 'borrow_api'

urlpatterns = [
    path('', BorrowBookView.as_view(), name="borrow_book"),
]