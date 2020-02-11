from django.contrib import admin

from . import models


@admin.register(models.MyBook)
class MyBookAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Memo)
class MemoAdmin(admin.ModelAdmin):
    pass
