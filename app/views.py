from django.shortcuts import render, get_object_or_404, redirect
from .models import Film, Actor, Director, Genre, Session, Ticket
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required


def main(request):
    return render(request, 'cinema/main.html')

def sessions(request):
    sessions_list = Session.objects.all()
    session_film = Film.objects.all()
    return render(request, 'cinema/sessions.html', {'sessions_list': sessions_list,
                                                                        'session_films': session_film})

def session_detail(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    return render(request, 'cinema/session_detail.html', {'session': session})

@login_required(login_url='login')
def purchase_ticket(request, session_id):
    if request.method == "POST":
        session = get_object_or_404(Session, pk=session_id)
        if session.tickets_total > 0:
            user = request.user
            Ticket.objects.create(ticket_price=session.ticket_price,
                                  session=session,
                                  user=user)
            session.tickets_total -= 1
            session.save()
            return redirect('my_tickets', user_id=user.id)
        else:
            return redirect('session_detail', session_id=session_id)

    return redirect('session_detail', session_id=session_id)

def film_detail(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    directors = film.director.all()
    actors = film.actors.all()
    genres = film.genre.all()
    return render(request, 'cinema/film_detail.html', {'film': film,
                                                                           'directors': directors,
                                                                           'actors': actors,
                                                                           'genres': genres})

def actor_detail(request, actor_id):
    actor = get_object_or_404(Actor, pk=actor_id)
    films = actor.films.all()
    return render(request, 'cinema/actor_detail.html', {'actor': actor, 'films': films})

def director_detail(request, director_id):
    director = get_object_or_404(Director, pk=director_id)
    films = director.films.all()
    return render(request, 'cinema/director_detail.html', {'director': director, 'films': films})

def film_by_genre(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    films = genre.film_set.all()
    return render(request, 'cinema/film_by_genre.html', {'genre': genre, 'films': films})

def actors(request):
    actors_list = Actor.objects.all()
    return render(request, 'cinema/actors.html', {'actors_list': actors_list})

def directors(request):
    directors_list = Director.objects.all()
    return render(request, 'cinema/directors.html', {'directors_list': directors_list})

def films(request):
    films_list = Film.objects.all()
    return render(request, 'cinema/films.html', {'films_list': films_list})

def genres(request):
    genres_list = Genre.objects.all()
    return render(request, 'cinema/genres.html', {'genres_list': genres_list})

@login_required(login_url='login')
def my_tickets(request, user_id):
    current_user = request.user
    if current_user.id != user_id:
        return render(request, 'cinema/my_tickets.html',
                      {'error': 'Вы не можете просматривать билеты других пользователей!'})

    user = User.objects.get(pk=user_id)
    tickets = Ticket.objects.filter(user=user)
    return render(request, 'cinema/my_tickets.html', {'user': user, 'tickets': tickets})

def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm

    return render(request, 'cinema/registration.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = AuthenticationForm()

    return render(request, 'cinema/login.html', {'form': form})