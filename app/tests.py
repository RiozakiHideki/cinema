from django.test import TestCase
from rest_framework.test import APIClient
from .models import Actor, Director, Genre, Film, Session, Ticket, User
import datetime
from django.urls import reverse

from .views import films


class ActorAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='example@example.com',
            password='Random_password_pass123'
        )

        self.actor = Actor.objects.create(
            name='test_actor_name',
            age=30,
            sex='male',
            image='',
        )

        self.director = Director.objects.create(
            name='test_director_name',
            age=30,
            sex='female',
            image='',
        )

        self.genre = Genre.objects.create(
            genre='test_genre_name',
        )

        self.film = Film.objects.create(
            name='test_film_name',
            description='test_description',
            release_date=datetime.date(2025, 1, 1),
            duration=120,
        )
        self.film.genre.add(self.genre)
        self.film.director.add(self.director)
        self.actor.films.add(self.film)
        self.film.actors.add(self.actor)
        self.director.films.add(self.film)

        film = Film.objects.get(id=1)
        start_time = datetime.datetime(year=2025, month=1, day=25, hour=18, minute=0)
        self.session = Session.objects.create(
            film=film,
            start_time=start_time,
            end_time=start_time + datetime.timedelta(minutes=film.duration),
            ticket_price=150,
            tickets_total=500,
            tickets_sold=0,
        )

        self.ticket = Ticket.objects.create(
            session=self.session,
            ticket_price=self.session.ticket_price,
            user=self.user,
        )

        self.client = APIClient()

    def test_films_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/films/')
        self.assertEqual(response.status_code, 200)
        print(response.content)

    def test_actors_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/actors/')
        self.assertEqual(response.status_code, 200)
        print(response.content)

    def test_directors_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/directors/')
        self.assertEqual(response.status_code, 200,)
        print(response.content)

    def test_genres_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/genres/')
        self.assertEqual(response.status_code, 200)
        print(response.content)

    def test_sessions_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/sessions/')
        self.assertEqual(response.status_code, 200)
        print(response.content)

    def test_tickets_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/tickets/')
        self.assertEqual(response.status_code, 200)
        print(response.content)

    def test_all_api_pages(self):
        api_pages = ['/api/films/',
                     '/api/actors/',
                     '/api/directors/',
                     '/api/genres/',
                     '/api/sessions/',
                     '/api/tickets/']
        self.client.force_authenticate(user=self.user)
        for i in api_pages:
            response = self.client.get(i)
            self.assertEqual(response.status_code, 200)
            print(response.content)

    def test_buy_ticket(self):
        self.client.login(username='tester', password='Random_password_pass123')
        data = {
            'session': self.session.id,
            'ticket_price': self.session.ticket_price,
            'user': self.user.id,
        }

        self.assertEqual(self.session.tickets_total, 500)

        response = self.client.post(f'/purchase_ticket/{self.session.id}/', data)
        self.assertEqual(response.status_code, 302)  # убеждаемся, что редирект происходит
        self.assertRedirects(response, f'/my_tickets/{self.user.id}/')  # успешная покупка
        self.session.refresh_from_db()  # обновляем бд
        self.assertEqual(self.session.tickets_total, 499)  # убеждаемся, что билет был куплен