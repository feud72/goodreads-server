# Generated by Django 3.0.3 on 2020-02-11 02:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_current_bookshelf'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shelves', '0003_auto_20200210_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mybook',
            name='bookshelf',
        ),
        migrations.AddField(
            model_name='mybook',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='BookShelf',
        ),
    ]
