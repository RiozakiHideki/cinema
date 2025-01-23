"""
URL configuration for Cinema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from app import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from app.views import (FilmViewSet, ActorViewSet, DirectorViewSet,
                      GenreViewSet, SessionViewSet, TicketViewSet)

router = DefaultRouter()
router.register(r'films', FilmViewSet)
router.register(r'actors', ActorViewSet)
router.register(r'directors', DirectorViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'sessions', SessionViewSet)
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),
    path('sessions/', views.sessions, name='sessions'),
    path('actor_detail/<int:actor_id>/', views.actor_detail, name='actor_detail'),
    path('director_detail/<int:director_id>/', views.director_detail, name='director_detail'),
    path('film_detail/<int:film_id>/', views.film_detail, name='film_detail'),
    path('film_by_genre/<int:genre_id>/', views.film_by_genre, name='film_by_genre'),
    path('session_detail/<int:session_id>/', views.session_detail, name='session_detail'),
    path('purchase_ticket/<int:session_id>/', views.purchase_ticket, name='purchase_ticket'),
    path('', views.main, name=''),
    path('actors/', views.actors, name='actors'),
    path('films/', views.films, name='films'),
    path('genres/', views.genres, name='genres'),
    path('directors/', views.directors, name='directors'),
    path('my_tickets/<int:user_id>/', views.my_tickets, name='my_tickets'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
]
