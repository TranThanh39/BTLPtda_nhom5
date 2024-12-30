from django.urls import path
from movie import views

app_name='movie'

urlpatterns = [
    path('', views.show_login, name='show_login'),
    path('signup', views.show_sign_up, name='show_sign_up'),
    path('procese_sign_up', views.sign_up, name='sign_up'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('forgotpass', views.show_forgot_pass, name='show_forgot_pass'),
    path('home', views.show_home, name='show_home'),
    path('movie', views.show_movie, name='show_movie'),
    path('news', views.show_news, name='show_news'),
    path('rap', views.show_rap, name='show_rap'),
    path('lich_chieu', views.show_lich, name='show_lich'),
    path('gia_ve', views.show_gia_ve, name='show_gia'),
    path('log_out', views.log_out, name='log_out'),
    path('movie_detail/<int:movie_id>', views.show_detail, name='movie_detail'),
    path('select', views.select_seat, name='select'),
    path('ve/<int:user_id>', views.show_ve, name='ve'),
    path('change_info', views.change_info, name='change'),
    path('change_in4', views.change_in4, name='changein4'),
    path('thanhtoan', views.thanhtoan, name='thanhtoan')
]
