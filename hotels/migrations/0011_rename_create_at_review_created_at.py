# Generated by Django 4.2 on 2023-04-06 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0010_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='create_at',
            new_name='created_at',
        ),
    ]
