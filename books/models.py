from django.db import models

from core.models import CoreModel


class Book(CoreModel):
    title = models.CharField(max_length=500, default="", blank=True)
    author = models.CharField(max_length=200, default="", blank=True)
    publisher = models.CharField(max_length=100, default="", blank=True)
    pub_year = models.CharField(max_length=20, default="", blank=True)
    isbn = models.CharField(max_length=13, primary_key=True)
    description = models.TextField(max_length=1000, default="", blank=True)
    bookImage = models.ImageField(upload_to="bookImage", blank=True, null=True)
    num_views = models.IntegerField(default=0)
    last_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def review_count(self):
        return self.review_set.distinct().count()

    @property
    def like_count(self):
        return self.mybook_set.distinct().count()
