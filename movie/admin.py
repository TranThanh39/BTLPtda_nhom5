from django.contrib import admin
from .models import * 
from .models import movie

# Register your models here.
# admin.site.register(users)
@admin.register(users)
class users(admin.ModelAdmin):
    list_display=('full_name', 'phone_number')
    search_fields=('phone_number',)

@admin.register(movie)
class movie(admin.ModelAdmin):
    list_display=('mov_name', 'mov_special')
    ordering=('mov_date', )

@admin.register(room)
class room(admin.ModelAdmin):
    list_display=('room_name', )

@admin.register(show)
class show(admin.ModelAdmin):
    list_display=('movie_for', 'room_for', 'date_show', 'hour_show')

    def message_user(self, request, message, level = ..., extra_tags = ..., fail_silently = ...):
        return
    
    
    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except ValidationError as e:
            messages.error(request, f"Lịch chiếu bạn chọn bị trùng với một lịch chiếu khác, vui lòng chọn thời gian khác hoặc phòng khác")
            return
        except Exception as e:
            messages.success(request, e)

        else:   
            return super().save_model(request, obj, form, change)


    

admin.site.register(seat)
admin.site.register(ticket)