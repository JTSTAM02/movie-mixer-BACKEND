from django.db import models

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
    

class User(models.Model):
    name=models.CharField(max_length=200)
    email= models.CharField(max_length=200)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.username


