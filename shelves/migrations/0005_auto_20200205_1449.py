# Generated by Django 3.0.3 on 2020-02-05 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelves', '0004_auto_20200205_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookshelf',
            name='gender',
            field=models.CharField(choices=[('M', '남성'), ('F', '여성'), ('N', '공개하지 않음')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='bookshelf',
            name='name',
            field=models.CharField(default='내 책장', max_length=30),
        ),
    ]
