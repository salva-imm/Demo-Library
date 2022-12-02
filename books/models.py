from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class BookCategory(models.Model):
    name = models.CharField(max_length=50)
    details = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.CharField(max_length=200)
    category = models.ManyToManyField(BookCategory)
    publisher = models.CharField(max_length=100)

    def __str__(self):
        return self.title + ' / ' + self.authors


class BookReview(models.Model):
    class Scores(models.IntegerChoices):
        VERY_BAD = 1
        BAD = 2
        AVERAGE = 3
        GOOD = 4
        AWSOME = 5

    review = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=CASCADE)
    score = models.SmallIntegerField(choices=Scores.choices)
    book = models.ForeignKey(Book, on_delete=CASCADE)

    class Meta:
        unique_together = [['user', 'book']]

    def __str__(self):
        return self.book.title + ' / ' + str(self.user) + ' : ' + str(self.score)
