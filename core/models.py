from django.db import models


class CoreModel(models.Model):

    created_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True
