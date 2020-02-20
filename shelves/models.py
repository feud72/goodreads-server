from django.db import models

from core.models import CoreModel


class MyBook(CoreModel):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True)
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    # finished = models.BooleanField(default=False)

    def __str__(self):
        return self.book.title
