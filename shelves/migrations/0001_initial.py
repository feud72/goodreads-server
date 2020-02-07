# Generated by Django 3.0.3 on 2020-02-07 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookShelf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('name', models.CharField(default='내 책장', max_length=30)),
                ('gender', models.CharField(choices=[('M', '남성'), ('F', '여성'), ('N', '공개하지 않음')], default='N', max_length=1)),
                ('age', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MyBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('finished', models.BooleanField(default=False)),
                ('current_page', models.IntegerField(default=0)),
                ('total_page', models.IntegerField(blank=True)),
                ('star', models.IntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Book')),
                ('bookshelf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shelves.BookShelf')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Memo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('page', models.IntegerField(default=0)),
                ('subject', models.CharField(max_length=100)),
                ('description', models.TextField(default='', max_length=1000)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shelves.MyBook')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
