import os
from random import randint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library.settings")

import django

django.setup()

from django.contrib.auth.models import User

from books.models import Book, BookCategory
from borrow.models import BookInstance, BorrowedBook

from faker import Faker
from model_bakery.recipe import Recipe, foreign_key

fake = Faker()
for c in ['novel', 'thriller', 'comedy', 'philosophy', 'science', 'technology']:
    BookCategory.objects.create(name=c)
for k in range(100):
    book = Recipe(Book,
                  title=fake.sentence(),
                  authors=fake.name(),
                  category=[BookCategory.objects.all().order_by('?').first()],
                  publisher=fake.name())
    instances = []
    for i in range(randint(0, 5)):
        instances.append(Recipe(BookInstance,
                                book=foreign_key(book)))
    for i in instances:
        i.make()
    if not instances:
        book.make()

for entry in range(200):
    data = fake.simple_profile()
    first_name, last_name, *_ = data['name'].split()
    user = User.objects.get_or_create(username=data['username'], first_name=first_name, last_name=last_name,
                                      email=data['mail'])

for reserve in range(150):
    borrowed_book = Recipe(BorrowedBook,
                           book=BookInstance.objects.all().order_by('?').first(),
                           user=User.objects.all().order_by('?').first())
    borrowed_book.make()
if __name__ == '__main__':
    pass
