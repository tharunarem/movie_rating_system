from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='movie_posters/', blank=True, null=True)  
    
    def average_rating(self):
        ratings = self.ratings.all()
        return sum(r.rating for r in ratings) / ratings.count() if ratings.exists() else 0

    def __str__(self):
        return self.title

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name="ratings", on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Ratings from 1 to 5

    class Meta:
        unique_together = ('user', 'movie')  # Prevents duplicate ratings by the same user

    def __str__(self):
        return f"{self.user.username} rated {self.movie.title}: {self.rating}"


class Dummy(models.Model):
    dummyname=models.CharField(max_length=100)
    age=models.IntegerField()
    