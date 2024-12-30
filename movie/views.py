from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import users, movie, seat, room, ticket, show
from datetime import date as datee, timedelta as timed
from datetime import datetime


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
    ngoaiquoc=[]
    vietnam=[]
    dacbiet=[]
    st1, st2, st3 = 0, 0, 0
    for i in movies:
        if st1==1 and st2==1 and st3==1:
            break
        if i.mov_region!='Việt Nam':
            if len(ngoaiquoc)==8:
                st1=1
                continue
            ngoaiquoc.append(i)
        else:
            if len(vietnam)==8:
                st2=1
                continue
            vietnam.append(i)
        if i.mov_special==True:
            if len(dacbiet)==8:
                st3=1
                continue
            dacbiet.append(i)
    return render(request, 'trangchu/trangchucdb.html' , { 'name':user_name, 'ngoaiquoc': ngoaiquoc, 'vietnam':vietnam, 'dacbiet':dacbiet, 'id':request.session['user_id']})

def show_movie(request):
    ngoaiquoc=[]
    vietnam=[]
    dacbiet=[]
    movies=movie.objects.all()
    for i in movies:
        if i.mov_region!="Việt Nam":
            ngoaiquoc.append(i)
        else:
            vietnam.append(i)
        if i.mov_special == True:
            dacbiet.append(i)
    if 'user_id' in request.session:
        id=request.session['user_id']
        user_name=users.objects.filter(id=id).values_list()[0][1]
        user_id=users.objects.filter(id=id).values_list()[0][0]
        return render(request, 'phimdangchieu.html', {'ngoaiquoc':ngoaiquoc, 'vietnam':vietnam, 'dacbiet': dacbiet, 'name':user_name,'id':user_id})
    return render(request, 'phimdangchieu.html', {'ngoaiquoc':ngoaiquoc, 'vietnam':vietnam, 'dacbiet': dacbiet})


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
    date=[]
    today=datee.today()
    current=today
    for i in range(10):
        date.append(today)
        today+=timed(days=1)
    if 'user_id' in request.session:
        id=request.session['user_id']
        user_name=users.objects.filter(id=id).values_list()[0][1]
        user_id=users.objects.filter(id=id).values_list()[0][0]
        return render(request, 'lich.html', {'movies':movies, 'date':date,  'name':user_name, 'id':user_id, 'current':current})
    return render(request, 'lich.html', {'movies':movies, 'date':date,  'current':current})

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
    tmp=show.objects.filter(movie_for=mov1)  
    dictt=dict()
    list_seat_checked=[]
    flag=0
    for i in tmp:
        if i.movie_for.mov_date>=datetime.now().date():
            flag=1
            
            dictt[(i.room_for.room_name+'-'+str(i.hour_show)) + ('pm' if i.hour_show>12 else 'am')]=seat.objects.filter(room_for=i.room_for)
        for j in ticket.objects.filter(show_for=i):
            list_seat_checked.append((i.room_for.room_name+'-'+str(i.hour_show)) + ('pm' if i.hour_show>12 else 'am') + str(j.seat_for.id))
    if flag==0:
        dictt=None
    if len(list_seat_checked)==0:
        list_seat_checked=None
    the_dict={'mov1':mov1, 'seats':dictt ,'checked': list_seat_checked}
    if 'user_id' in request.session:
        id=request.session['user_id']
        user_name=users.objects.filter(id=id).values_list()[0][1]
        user_id=users.objects.filter(id=id).values_list()[0][0]
        the_dict['id']=user_id
        the_dict['name']=user_name
        return render(request, 'phimSapChieu1.html', the_dict)
    return render(request, 'phimSapChieu1.html', the_dict)


def select_seat(request):
    if request.method == 'POST':
        if (not 'user_id' in request.session) or (not request.session.keys()):
            return redirect('movie:show_login')
        seat_id=request.POST.get('id').split(',')
        seat_id.pop()
        for i in range(len(seat_id)):
            for j in range(len(seat_id[i])):
                if seat_id[i][j] == 'm':
                    seat_id[i]=((seat_id[i][:j+1]+'-'+seat_id[i][j+1:]).split('-'))
                    break
        
        moviee=movie.objects.get(id=request.POST.get('mov_id'))
        cost = moviee.mov_cost*len(seat_id)
        if 'user_id' in request.session:
            id=request.session['user_id']
            user_name=users.objects.filter(id=id).values_list()[0][1]
            return render(request, 'thanhtoan.html', {'seats':seat_id, 'movie':moviee, 'name':user_name, 'id':id, 'cost':cost})
        return render(request, 'thanhtoan.html', {'seats':seat_id, 'movie':moviee})


def thanhtoan(request):
    if request.method == 'POST':
        list_ve=request.POST.get('name1')
        import ast

        list_ve = ast.literal_eval(list_ve)
        for i in list_ve:
            tmp=i[1]
            if 'am' in tmp:
                tmp=tmp.replace('am', '')
            if 'pm' in tmp:
                tmp=tmp.replace('pm', '')
            list_show=show.objects.filter(hour_show=tmp)
            for j in list_show:
                if j.room_for.room_name==i[0]:
                    tmp=j
            try:
                tmp.watcher+=1
                tmp.save()
            except Exception as e:
                pass
            try:
                tmp2=tmp.movie_for
                tmp2.mov_watcher+=1
                tmp2.save()
            except Exception as e:
                pass

            ticket.objects.create(user_for=users.objects.get(id=request.session['user_id']), seat_for=seat.objects.get(id=i[2]), show_for=tmp)

            return redirect('movie:ve', user_id=request.session['user_id'])

def show_ve(request, user_id):
    tickets=ticket.objects.filter(user_for=users.objects.get(id=user_id))
    
    if 'user_id' in request.session:
        id=request.session['user_id']
        user_name=users.objects.filter(id=id).values_list()[0][1]
        return render(request, 've.html', {'name':user_name, 'tickets':tickets, 'id':user_id})
    return render(request, 've.html', {'tickets':tickets, 'id':user_id})


def change_info(request):
    user=users.objects.get(id=request.session['user_id'])
    return render (request, 'formtt.html', {'user':user})


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
    