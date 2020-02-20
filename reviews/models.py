from django.db import models

from core.models import CoreModel


class Review(CoreModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    star = models.IntegerField(blank=True, null=True)
    description = models.TextField(max_length=1000, default="", null=True, blank=True)

    def __str__(self):
        return f'"{self.book.title}" # {self.user.nickname}님'
