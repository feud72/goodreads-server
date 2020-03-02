from django.contrib import admin

from . import models


@admin.register(models.Keyword)
class KeywordAdmin(admin.ModelAdmin):
    pass
