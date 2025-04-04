from django.db import models
from django.contrib.auth.models import User
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class BaseModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    sex = models.CharField(max_length=6)
    image = models.ImageField(upload_to='images/', default='')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Actor(BaseModel):
    films = models.ManyToManyField('Film', related_name='actor_films')

    def __str__(self):
        return f"{self.name}"

class Director(BaseModel):
    films = models.ManyToManyField('Film', related_name='director_films')

class Genre(models.Model):
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.genre

class Film(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True)
    release_date = models.DateField()
    director = models.ManyToManyField(Director, related_name='directed_films')
    genre = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor, related_name='acted_films')
    duration = models.IntegerField()  # minutes

    def __str__(self):
        return self.name

class Session(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    ticket_price = models.IntegerField(default=300)
    tickets_total = models.IntegerField(default=500)
    tickets_sold = models.IntegerField(default=0)

    def __str__(self):
        return f"Session for {self.film.name} at {self.start_time}"

class Ticket(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    ticket_price = models.IntegerField(default=10, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Ticket for {self.session} by {self.user.username}"
