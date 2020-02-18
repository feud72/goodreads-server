from django.db import models

from core.models import CoreModel


class MyBook(CoreModel):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True)
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title


class Review(CoreModel):
    book = models.OneToOneField(MyBook, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    star = models.IntegerField(blank=True, null=True)
    description = models.TextField(max_length=1000, default="", null=True, blank=True)

    def __str__(self):
        return f': "{self.book.book.title}" # {self.book.owner.nickname}님'
