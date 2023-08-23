from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class movie(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    description = models.TextField()
    class Meta:
        app_label = 'movie'
    def __str__(self):
        return self.title
    
class CustomUser(AbstractUser):
    def __str__(self):
        return self.username


class User(models.Model):
    name=models.CharField(max_length=200)
    email= models.CharField(max_length=200)
    password = models.CharField(max_length=50)
    date_registered = models.DateTimeField(null=True)

    
    def __str__(self):
        return self.username

class UserLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exercise_id = models.CharField(max_length=100)
    date_completed = models.DateTimeField()
    total_questions = models.CharField(max_length=100)
    correct_answers = models.CharField(max_length=100)
