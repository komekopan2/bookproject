# Generated by Django 4.1.7 on 2023-04-02 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0009_book_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
