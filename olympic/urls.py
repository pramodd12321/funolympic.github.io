from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [

path('', views.home, name="home"),
path('news/', views.newsindex, name="news"),
path('login/', views.SigninPage, name="login"),
path('signup/', views.SignupPage, name="signup"),
path('signout/', views.SignoutUser, name="logout"),

path('token/', views.send_token, name="send_token"),
path('success/', views.success, name="success"),
path('verify/<auth_token>' , views.verify , name="verify"),
path('error' , views.error_page , name="error"),
path('dashboard/', views.dashboard, name="dashboard"),

path('reset_password/',
auth_views.PasswordResetView.as_view(template_name="olympic/password_reset.html"),
name="reset_password"),

path('reset_password_sent/', 
    auth_views.PasswordResetDoneView.as_view(template_name="olympic/password_reset_sent.html"), 
    name="password_reset_done"),

path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="olympic/password_reset_form.html"), 
    name="password_reset_confirm"),

path('reset_password_complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name="olympic/password_reset_done.html"), 
    name="password_reset_complete"),


path('test/', views.test, name="hom"),


path('user/', views.user, name="user"),
path('Football_Scoreboard/<int:myid>', views.fscoreboard, name="football_scoreboard"),
path('PostComment', views.PostComment, name="Postcomment"),
path('dashboard/football/', views.football, name="football"),

path('matches/', views.matches, name="matches"),
path('lvideos/', views.lvideos, name="lvideos"),
path('videos1/<int:video_id>/', views.videos1, name="videos1"),
path('videos1/add_comment/', views.add_comment, name='add_comment'),

path('notifications/', views.get_noti, name='notifications'),

path('videos/add_comment/', views.add_comment, name='add_comment'),

path('videos2/<int:video_id>/', views.videos2, name="videos2"),
path('videos2/add_comment/', views.add_comment, name='add_comment'),

path('videos2/add_like/', views.add_like, name='add_like'),

]
