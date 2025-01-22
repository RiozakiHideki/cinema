from rest_framework import serializers
from .models import Film, Actor, Director, Genre, Session, Ticket

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'genre']

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name', 'age', 'sex', 'image', 'films']
        
class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name', 'age', 'sex', 'image', 'films']

class FilmSerializer(serializers.ModelSerializer):
    directors = DirectorSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Film
        fields = ['id', 'name', 'description', 'release_date', 'duration', 
                 'directors', 'genres', 'actors']

class SessionSerializer(serializers.ModelSerializer):
    film = FilmSerializer(read_only=True)
    
    class Meta:
        model = Session
        fields = ['id', 'film', 'start_time', 'end_time', 
                 'ticket_price', 'tickets_available']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'session', 'user', 'purchase_date']
        read_only_fields = ['user', 'purchase_date']