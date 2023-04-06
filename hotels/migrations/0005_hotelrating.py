# Generated by Django 4.2 on 2023-04-06 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotels', '0004_hotel_bookings_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='hotels.hotel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_ratings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Рейтинг отеля',
                'verbose_name_plural': 'Рейтинги отелей',
                'unique_together': {('user', 'hotel')},
            },
        ),
    ]
