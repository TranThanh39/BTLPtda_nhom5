from django.db import models
from django.utils.text import slugify


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
    mov_date=models.DateField(null=True)
    mov_cost=models.IntegerField()
    mov_type=models.CharField(max_length=50)
    mov_image=models.CharField(max_length=200)
    mov_video=models.CharField(max_length=200)
    mov_duration=models.IntegerField()
    mov_region=models.CharField(max_length=20)
    mov_watcher=models.IntegerField(default=0)
    mov_status=models.IntegerField(default=0)

    # def save(self, *args, **kwargs):
    #     if self.pk is None:
    #         tmp2=1
    #     else:
    #         tmp2=2
    #     tmp = super().save(*args, **kwargs)
    #     print (tmp2)
    #     if tmp2==1:
    #         for i in range(1,61):
    #             seat.objects.create(seat_name=str(i), status=False, mov_foreign=self)
    #     return tmp
    def __str__(self):
        return self.mov_name


class room(models.Model):
    room_name=models.CharField(max_length=10)
    movie=models.ForeignKey(movie, on_delete=models.CASCADE, null=True)
    def save(self, *args, **kwargs):
        if self.pk is None:
            super().save(*args, **kwargs)
            for i in range(1,61):
                seat.objects.create(seat_name=str(i), status=False, room_foreign=self)
        else:
            old_movie=room.objects.get(pk=self.pk).movie
            super().save(*args, **kwargs)
            if old_movie!=self.movie:
                print('**************************')
                tmp=seat.objects.filter(room_foreign_id=self.id)
                for i in tmp:
                    print(i, '*****')
                seat.objects.filter(room_foreign=self).delete()
                ticket.objects.filter()
                for i in range(1,61):
                    seat.objects.create(seat_name=str(i), status=False, room_foreign=self)
        print(self.movie)
        


class seat(models.Model):
    seat_name=models.CharField(max_length=10)
    status=models.BooleanField()  
    # used=models.ForeignKey(users, on_delete=models.CASCADE, null=True)
    # mov_foreign=models.ForeignKey(movie, on_delete=models.CASCADE)
    room_foreign=models.ForeignKey(room, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.room_foreign.room_name+'-'+self.seat_name



class ticket(models.Model):
    user=models.ForeignKey(users, on_delete=models.CASCADE, null=True)
    seat=models.ForeignKey(seat, on_delete=models.CASCADE, null=True)
   
        
