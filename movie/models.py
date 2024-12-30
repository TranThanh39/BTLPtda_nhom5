from django.db import models
from django.contrib import messages
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import datetime



class users(models.Model):
    full_name=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=10)
    email=models.EmailField()
    pass_word=models.CharField(max_length=50)
    date_of_birth=models.DateField()
    sex=models.CharField(max_length=10)

    def __str__(self):
        return self.full_name




class movie(models.Model):
    mov_name=models.CharField(max_length=100)
    mov_description=models.CharField(max_length=100)
    mov_date=models.DateField()
    mov_cost=models.IntegerField()
    mov_type=models.CharField(max_length=50)
    mov_image=models.CharField(max_length=200)
    mov_video=models.CharField(max_length=200)
    mov_duration=models.IntegerField()
    mov_region=models.CharField(max_length=20)
    mov_watcher=models.IntegerField(default=0)
    mov_special=models.BooleanField(default=False)
    def __str__(self):
        return self.mov_name


class room(models.Model):
    room_name=models.CharField(max_length=10)
    def save(self, *args, **kwargs):
        if self.pk is None:
            super().save(*args, **kwargs)
            for i in range(1,61):
                seat.objects.create(seat_name=str(i), status=False, room_for=self)
        else:
            old_movie=room.objects.get(pk=self.pk).movie
            super().save(*args, **kwargs)
            if old_movie!=self.movie:
                seat.objects.filter(room_foreign=self).delete()
                ticket.objects.filter()
                for i in range(1,61):
                    seat.objects.create(seat_name=str(i), status=False, room_for=self)
    def __str__(self):
        return self.room_name
        

class show(models.Model):
    current_date = datetime.date.today()
    date_str = current_date.strftime("%Y-%m-%d")
    date_show=models.DateField(default=date_str)
    hour_show=models.IntegerField(choices=[(8, '8h'), (9, '9h'), (13, '13h'), (18, '18h'), (20, '20h')])
    room_for=models.ForeignKey(room, on_delete=models.CASCADE)
    movie_for=models.ForeignKey(movie, on_delete=models.CASCADE)
    watcher=models.IntegerField(default=0)


    def save(self, *args, **kwargs):
        tmp = show.objects.filter(room_for=self.room_for)
        for i in tmp:
            if i.id != self.id and i.date_show==self.date_show and abs(i.hour_show - self.hour_show)<=3:
                raise ValidationError(i.hour_show)
        raise Exception("Lưu thành công")
    
    def __str__(self):
        return self.movie_for.mov_name + '-' + self.room_for.room_name + '-' + str(self.hour_show) + 'pm' if self.hour_show > 12 else 'am' 

class seat(models.Model):
    seat_name=models.CharField(max_length=10)
    status=models.BooleanField(default=False)  
    room_for=models.ForeignKey(room, on_delete=models.CASCADE)

    def __str__(self):
        return self.room_for.room_name+'-'+self.seat_name



class ticket(models.Model):
    user_for=models.ForeignKey(users, on_delete=models.CASCADE)
    seat_for=models.ForeignKey(seat, on_delete=models.CASCADE)
    show_for=models.ForeignKey(show, on_delete=models.CASCADE)
    current_date = datetime.date.today()
    date_str = current_date.strftime("%Y-%m-%d")
    date=models.DateField(default=date_str)

    def __str__(self):
        return self.user_for.full_name+'-'+self.show_for.__str__()+'-'+self.seat_for.seat_name
   
        
