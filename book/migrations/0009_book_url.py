# Generated by Django 4.1.7 on 2023-04-02 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_alter_book_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
