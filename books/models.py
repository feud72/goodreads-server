from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=500, default="", blank=True)
    author = models.CharField(max_length=200, default="", blank=True)
    publisher = models.CharField(max_length=100, default="", blank=True)
    pub_year = models.CharField(max_length=20, default="", blank=True)
    volume = models.CharField(max_length=10, default="", blank=True)
    isbn = models.CharField(max_length=13, primary_key=True)
    kdc = models.CharField(max_length=10, default="", blank=True)
    description = models.TextField(max_length=1000, default="", blank=True)

    def __str__(self):
        return self.title
