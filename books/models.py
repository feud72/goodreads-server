from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=500, default="")
    author = models.CharField(max_length=200, default="")
    publisher = models.CharField(max_length=100, default="")
    pub_year = models.CharField(max_length=20, default="")
    volume = models.CharField(max_length=10, default="")
    isbn = models.CharField(max_length=13, primary_key=True)
    kdc = models.CharField(max_length=10, default="")
    description = models.TextField(max_length=1000, default="")

    def __str__(self):
        return self.title
