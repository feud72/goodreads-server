from django.contrib import admin

from . import models


@admin.register(models.MyBook)
class MyBookAdmin(admin.ModelAdmin):
    pass
