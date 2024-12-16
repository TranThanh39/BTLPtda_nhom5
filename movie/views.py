from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import users, movie, seat, room, ticket
from datetime import date as datee, timedelta as timed

def show_login(request):
    return render(request, 'Sign-in.html')

def show_sign_up(request):
    return render(request, 'Sign-up.html')

def show_forgot_pass(request):
    return render(request, 'Forgot_pass.html')

def show_home(request):
    id=request.session['user_id']
    user_name=users.objects.filter(id=id).values_list()[0][1]
    movies=movie.objects.all().order_by('-mov_watcher')
    dangchieu=[]
    sapchieu=[]
    dacbiet=[]
    st1, st2, st3 = 0, 0, 0
    for i in movies:
        if st1==1 and st2==1 and st3==1:
            break
        if i.mov_status==0:
            if len(dangchieu)==8:
                st1=1
                continue
            dangchieu.append(i)
        elif i.mov_status==1:
            if len(sapchieu)==8:
                st2=1
                continue
            sapchieu.append(i)
        else:
            if len(dacbiet)==8:
                st3=1
                continue
            dacbiet.append(i)
    return render(request, 'trangchu/trangchucdb.html' , { 'name':user_name, 'dangchieu': dangchieu, 'sapchieu':sapchieu, 'dacbiet':dacbiet, 'id':request.session['user_id']})

def show_movie(request):
    dangchieu=[]
    sapchieu=[]
    dacbiet=[]
    movies=movie.objects.all()
    for i in movies:
        if i.mov_status==0:
            dangchieu.append(i)
        elif i.mov_status==1:
            sapchieu.append(i)
        else:
            dacbiet.append(i)
    if 'user_id' in request.session:
        id=request.session['user_id']
        user_name=users.objects.filter(id=id).values_list()[0][1]
        user_id=users.objects.filter(id=id).values_list()[0][0]
        return render(request, 'phimdangchieu.html', {'dangchieu':dangchieu, 'sapchieu':sapchieu, 'dacbiet': dacbiet, 'name':user_name,'id':user_id})
    return render(request, 'phimdangchieu.html', {'dangchieu':dangchieu, 'sapchieu':sapchieu, 'dacbiet': dacbiet})


def show_news(request):
    if 'user_id' in request.session:
        id=request.session['user_id']
        user_name=users.objects.filter(id=id).values_list()[0][1]
        user_id=users.objects.filter(id=id).values_list()[0][0]

        return render(request,'tintuc.html', {'name':user_name, 'id':user_id})
    return render(request, 'tintuc.html')


def show_rap(request):
    movies=movie.objects.all().order_by('-mov_watcher')[0:4]
    if 'user_id' in request.session:
        id=request.session['user_id']
        user_name=users.objects.filter(id=id).values_list()[0][1]
        user_id=users.objects.filter(id=id).values_list()[0][0]
        return render(request, 'Rap_layout.html', {'movies': movies,'name':user_name, 'id':user_id})
    return render(request, 'Rap_layout.html', {'movies': movies})

def show_lich(request):
    movies=movie.objects.all().order_by('mov_date')
    movie_sap=[]
    date=[]
    for i in movies:
        if i.mov_status==2:
            movie_sap.append(i)
    today=datee.today()
    for i in range(10):
        date.append(today)
        today+=timed(days=1)
    if 'user_id' in request.session:
        id=request.session['user_id']
        user_name=users.objects.filter(id=id).values_list()[0][1]
        user_id=users.objects.filter(id=id).values_list()[0][0]
        return render(request, 'lich.html', {'movies':movies, 'date':date, 'movie_sap':movie_sap, 'name':user_name, 'id':user_id})
    return render(request, 'lich.html', {'movies':movies, 'date':date, 'movie_sap':movie_sap})

def show_gia_ve(request):
    if 'user_id' in request.session:
        id=request.session['user_id']
        user_name=users.objects.filter(id=id).values_list()[0][1]
        user_id=users.objects.filter(id=id).values_list()[0][0]
        return render(request, 'GiaVe.html', {'id':user_id, 'name':user_name})
    return render(request, 'GiaVe.html')


def sign_up(request):
    if request.method == 'POST':
        fullname=request.POST.get('fullname')
        phonenumber=request.POST.get('phonenumber')
        email=request.POST.get('email')
        password=request.POST.get('password')
        repassword=request.POST.get('repassword')
        dateofbirth=request.POST.get('dateofbirth')
        sex=request.POST.get('sex')
        policy=request.POST.get('policy')
        if users.objects.filter(email=email).exists():
            messages.info(request, 'Email đã tồn tại')
            return redirect('movie:show_sign_up')
        else:
            if password != repassword:
                messages.info(request, 'Mật khẩu không trùng khớp')
                return redirect('movie:show_sign_up')
            else:
                if policy is None:
                    messages.info(request, 'Xin hãy đồng ý với chính sách')
                    return redirect('movie:show_sign_up')
                else:
                    new_user=users(full_name=fullname, phone_number=phonenumber, email=email, pass_word=password, date_of_birth=dateofbirth, sex=sex)
                    new_user.save()
                    messages.info(request, 'Đăng ký thành công')
                    return redirect('movie:show_login')


def sign_in(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        pass_word=request.POST.get('password')
        userss=list(users.objects.all().values_list())
        for i in userss:
            if email==i[3]:
                if pass_word==i[4]:
                    request.session['user_id']=i[0]
                    return redirect('movie:show_home')
                else:
                    messages.info(request, 'Mật khẩu không chính xác')
                    return redirect('movie:show_login')
        messages.info(request, 'Email chưa được đăng ký')
        return redirect('movie:show_login')    


def log_out(request):
    request.session.delete()
    return redirect('movie:show_login')


def show_detail(request, movie_id):
    mov1=movie.objects.get(id=movie_id)
    tmp=room.objects.filter(movie=mov1)
    dictt=dict()
    for i in tmp:
        dictt[i.room_name]=seat.objects.filter(room_foreign=i)
    print(dictt)
    if 'user_id' in request.session:
        id=request.session['user_id']
        user_name=users.objects.filter(id=id).values_list()[0][1]
        user_id=users.objects.filter(id=id).values_list()[0][0]
        return render(request, 'phimSapChieu1.html', {'id': user_id, 'name':user_name, 'mov1':mov1, 'seats':dictt})
    return render(request, 'phimSapChieu1.html', {'mov1':mov1, 'seats':dictt})


def select_seat(request):
    if request.method == 'POST':
        if not request.session.keys():
            return redirect('movie:show_login')
        seat_id=request.POST.get('id')
        seatt=seat.objects.get(id=seat_id)
        seatt.status=True
        moviee=movie.objects.get(id=room.objects.get(id=seatt.room_foreign_id).movie_id)
        moviee.mov_watcher+=1
        ticket.objects.create(user=users.objects.get(id=request.session['user_id']),seat=seatt)
        seatt.save()
        moviee.save()
        return redirect('movie:ve', user_id=request.session['user_id'])


def show_ve(request, user_id):
    tickets=ticket.objects.filter(user_id=user_id)
    movies=[]
    seats=[]
    for i in tickets.values_list():
        movies.append(movie.objects.get(id=room.objects.get(id=seat.objects.get(id=i[2]).room_foreign_id).movie_id))
        tmp=seat.objects.get(id=i[2])
        seats.append(str(room.objects.get(id=tmp.room_foreign_id).room_name)+'-'+str(tmp.seat_name))
    combine=zip(seats, movies)
    if 'user_id' in request.session:
        id=request.session['user_id']
        user_name=users.objects.filter(id=id).values_list()[0][1]
        return render(request, 've.html', {'name':user_name, 'combine':combine, 'id':user_id})
    return render(request, 've.html', {'combine':combine, 'id':user_id})


def change_info(request):
    user=users.objects.get(id=request.session['user_id'])
    return render (request, 'formtt.html', {'user':user})

from datetime import datetime

def change_in4(request):
    if request.method=='POST':
        user=users.objects.get(id=request.session['user_id'])
        user.full_name=request.POST.get('fullname2')
        tmp=datetime.strptime(request.POST.get('birthdate2'), '%d/%m/%Y')
        user.date_of_birth=tmp.strftime('%Y-%m-%d')
        user.email=request.POST.get('email')
        user.phone_number=request.POST.get('phone')
        if len(request.POST.get('password')) != 0:
            user.pass_word=request.POST.get('password')
        user.sex=request.POST.get('gender')
        user.save()
        
    return redirect('movie:show_home')
    