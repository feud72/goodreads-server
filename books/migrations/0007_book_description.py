# Generated by Django 3.0.3 on 2020-02-07 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_auto_20200206_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
