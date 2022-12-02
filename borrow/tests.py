from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from faker import Faker
import random


from borrow.api.views import BorrowBookView
from books.models import Book, BookCategory
from borrow.models import BookInstance, BorrowedBook

# Create your tests here.
class BorrowedBookTests(TestCase):
    data = {
        "book": 0
    }
    def setUp(self):
        fake = Faker()
        self.factory = APIRequestFactory()
        self.view = BorrowBookView.as_view()
        book_category = BookCategory.objects.create(name="history")
        self.books = []
        mylist = [1,24,46,3]
        for item in range(4):
            book = Book.objects.create(
                title=fake.name(),
                authors=fake.name(),
                publisher=fake.name()
            )
            amval_code = random.choice(mylist)
            mylist.remove(amval_code)
            book.category.add(book_category)
            book_inst = BookInstance.objects.create(
                book=book,
                amval_code=amval_code
            )
            self.books.append(book_inst)
        self.user = User.objects.create_user(
            username="xyz",
            email="xyz@xyz.co",
            password="mypass"
        )
    def test_is_not_user_authenticated(self):
        request = self.factory.post('/borrow/', self.data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, 401)
    def test_can_borrow_book(self):
        self.data['book'] = self.books[0].id
        request = self.factory.post('/borrow/', self.data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_can_borrow_not_existing_book(self):
        self.data['book'] = 10000
        request = self.factory.post('/borrow/', self.data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 404)

    def test_expected_error_on_borrowing_more_that_three_book(self):
        # create 3 borrowed books for user
        for i in range(3):
            BorrowedBook.objects.create(
                user=self.user,
                book=self.books[i]
            )
        self.data['book'] = self.books[3].id
        request = self.factory.post('/borrow/', self.data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        response.render()
        msg = response.content.decode()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(msg,
                         '{"non_field_errors":["You can\'t borrow more than 3 book at the same time"]}'
                         )
