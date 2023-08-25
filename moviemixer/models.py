from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings


class User(AbstractUser):
    user_created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(max_length=255)

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    release_year = models.DateField()
    description = models.TextField()
    trailer_link = models.URLField()
    length_in_minutes = models.PositiveIntegerField()
    movie_rating = models.CharField(max_length=10)


class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)









class CustomUser(AbstractUser):
    def __str__(self):
        return self.username


class User(models.Model):
    name=models.CharField(max_length=200)
    email= models.CharField(max_length=200)
    password = models.CharField(max_length=50)
    date_registered = models.DateTimeField(null=True)

class UserLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exercise_id = models.CharField(max_length=100)
    date_completed = models.DateTimeField()
    total_questions = models.CharField(max_length=100)
    correct_answers = models.CharField(max_length=100)
