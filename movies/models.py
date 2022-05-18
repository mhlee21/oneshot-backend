from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Video(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=100)
    size = models.IntegerField()
    type = models.CharField(max_length=20)
    official = models.BooleanField()
    

class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    overview = models.TextField()
    adult = models.BooleanField()
    popularity = models.FloatField()
    backdrop_path = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=100)
    video = models.ManyToManyField(Video, related_name="movie_videos")
    genres = models.ManyToManyField(Genre, related_name="movie_genres")
    # runtime = models.IntegerField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()

    def __str__(self):
        return self.title