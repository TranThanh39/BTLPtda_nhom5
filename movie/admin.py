from django.contrib import admin
from .models import users, movie, seat, room, ticket

# Register your models here.
# admin.site.register(users)
@admin.register(users)
class users(admin.ModelAdmin):
    list_display=('full_name', 'phone_number')
    search_fields=('phone_number',)

@admin.register(movie)
class movie(admin.ModelAdmin):
    list_display=('mov_name', 'mov_status')
    ordering=('mov_date', )

@admin.register(room)
class room(admin.ModelAdmin):
    list_display=('room_name', 'movie_id')

admin.site.register(seat)
admin.site.register(ticket)