# Generated by Django 3.0.3 on 2020-02-10 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_book_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]