from django.core.management import BaseCommand
import datetime
from app.models import Actor, Director, Genre, Film, Session
from ._data import actors_data, films_data, directors_data

class Command(BaseCommand):
    def handle(self, *args, **options):

        def age_calc(birthday):
            current_date = datetime.datetime.now()
            age = current_date.year - birthday.year
            if (current_date.month, current_date.day) < (birthday.month, birthday.day):
                age -= 1
            return age

        # Актёры
        print("Создание актёров...")
        actors = []
        for actor_data in actors_data:
            actor = Actor.objects.create(
                name=actor_data['name'],
                age=age_calc(actor_data['birthday']),
                sex=actor_data['sex'],
                image=f'/images/{actor_data["image"]}',
            )
            actors.append(actor)
        print("Актёры успешно созданы.")

        # Режиссёры
        print("Создание режиссёров...")
        directors = []
        for director_data in directors_data:
            director = Director.objects.create(
                name=director_data['name'],
                age=age_calc(director_data['birthday']),
                sex=director_data['sex'],
                image=f'/images/{director_data["image"]}',
            )
            directors.append(director)
        print("Режиссёры успешно созданы.")

        # Жанры
        print("Создание жанров...")
        genres_dict = {}
        for film_data in films_data:
            for genre in film_data['genres']:
                if genre not in genres_dict:
                    genres_dict[genre] = Genre.objects.create(genre=genre)
        print("Жанры успешно созданы.")

        # Фильмы
        print("Создание фильмов...")
        for film_data in films_data:


            # Создание фильма
            film = Film.objects.create(
                name=film_data['title'],
                description='Тут должно быть описание, но мне лень его копипастить',
                release_date=film_data['release_date'],
                duration=film_data['duration'],
            )

            # Добавление режиссёра
            directors_to_add = [director for director in directors if director.name in film_data['director']]
            film.director.add(*directors_to_add)

            # Добавление жанров
            film.genre.add(*[genres_dict[genre] for genre in film_data['genres']])

            # Добавление актёров
            actors_to_add = [actor for actor in actors if actor.name in film_data['actors']]
            film.actors.add(*actors_to_add)

            # Добавление фильма актёрам
            for actor in actors_to_add:
                actor.films.add(film)  # Здесь мы добавляем фильм актёрам

            # Добавление фильма режиссёрам
            for director in directors_to_add:
                director.films.add(film)

        print("Фильмы успешно созданы.")

        # Сессии
        print("Создание сеансов...")
        for i in [1, 17, 19, 35]:
            film = Film.objects.get(id=i)
            start_time = datetime.datetime(year=2025, month=1, day=25, hour=15, minute=0)
            end_time = start_time + datetime.timedelta(minutes=film.duration)
            Session.objects.create(film = film,
                                   start_time = start_time,
                                   end_time = end_time,
                                   ticket_price=150,
                                   tickets_total=500,
                                   tickets_sold=0)

        print("Сеансы успешно созданы.")

        print("Билеты рандомно генерить смысла не вижу")
