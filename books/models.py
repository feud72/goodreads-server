from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=100)
    pub_year = models.CharField(max_length=20, blank=True, null=True)
    volume = models.CharField(max_length=10, blank=True, null=True)
    isbn = models.CharField(max_length=13, primary_key=True)
    kdc = models.CharField(max_length=10)

    def __str__(self):
        return self.name
