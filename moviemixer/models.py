from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.DateField()
    description = models.TextField()
    image = models.URLField(max_length=300, null=True)
    userRating = models.DecimalField(max_digits=3, decimal_places=1, default=None)
    trailerLink = models.URLField(max_length=300, null=True)

class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


class CustomUser(AbstractUser):
    user_created = models.DateTimeField(default=None, null=True)
    class Meta:
        db_table = 'auth_user'


