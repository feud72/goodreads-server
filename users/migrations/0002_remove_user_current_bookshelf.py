# Generated by Django 3.0.3 on 2020-02-11 02:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='current_bookshelf',
        ),
    ]
