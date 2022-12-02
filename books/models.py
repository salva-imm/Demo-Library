from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class BookCategory(models.Model):
    name = models.CharField(max_length=50)
    details = models.TextField(null=True, blank=True)


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.CharField(max_length=200)
    category = models.ManyToManyField(BookCategory)
    publisher = models.CharField(max_length=100)


class BookReview(models.Model):
    review = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=CASCADE)
    score = models.SmallIntegerField()
    book = models.ForeignKey(Book, on_delete=CASCADE)

    class Meta:
        unique_together = [['user', 'book']]
