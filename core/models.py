from django.db import models


class CoreModel(models.Model):

    created = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True
