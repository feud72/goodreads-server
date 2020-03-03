from django.db import models


class Keyword(models.Model):
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    weight = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["word"]

    def __str__(self):
        return f"{self.book.title} # {self.word}"
