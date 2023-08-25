# Generated by Django 4.2.4 on 2023-08-25 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moviemixer', '0002_genre_movie_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='length_in_minutes',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='movie_rating',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='trailer_link',
        ),
        migrations.DeleteModel(
            name='UserLog',
        ),
    ]