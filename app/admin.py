from django.contrib import admin
from .models import Film, Actor, Director, Genre, Session, Ticket

admin.site.register(Film)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Genre)
admin.site.register(Session)
admin.site.register(Ticket)