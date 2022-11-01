# Importing all required libraries.

from django.shortcuts import render, HttpResponse
from channels.layers import get_channel_layer
import json
import requests
from django.template import RequestContext

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .google_captcha import CaptchaForm
from .forms import CreateUserForm

from .models import *
import uuid

from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from .decorators import unauthenticated_user, allowed_users, admin_only


from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .forms import VideoForm
from django.core.exceptions import ObjectDoesNotExist



def mail(request):
	username = request.POST.get('username')
	email = request.POST.get('email')
	password = request.POST.get('password')
	user_obj = User.objects.create(username = username, email = email)
	user_obj.set_password(password)
	user_obj.save()
	auth_token = str(uuid.uuid4())
	profile_obj = Profile.objects.create(user = user_obj, auth_token = auth_token)
	profile_obj.save()
	send_mail_after_registration(email, auth_token)
	return redirect('/token')


def SignupPage(request):
	form = CreateUserForm()
    
	if request.method == 'POST':
		form = CreateUserForm(request.POST) 
		cform = CaptchaForm(request.POST)
		email = request.POST.get('email')

		
		if User.objects.filter(email = email).first():
			messages.error(request, "Email already exists!")
	

		elif form.is_valid() and cform.is_valid(): 
			email = request.POST.get('email')
			username = request.POST.get('username')

			auth_token = str(uuid.uuid4())
			send_mail_after_registration(email, auth_token) 
			user_obj = User.objects.create(username = username, email = email)
			user_obj.set_password(form.data.get('password1'))
			user_obj.save()
			profile_obj = Profile.objects.create(user = user_obj, auth_token = auth_token)
			profile_obj.save()
			# form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + user)
			
			return redirect('/token')

		else:
			messages.error(request, "Invalid captcha!")
		
	context = {
		'form': form,
		"captcha": CaptchaForm
		}

	return render(request, 'olympic/SignUp.html', context)


def success(request):
	return render(request, 'olympic/success.html')

def send_token(request):
	return render(request, 'olympic/send_token.html')


def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'error.html')


def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )



def SigninPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('dashboard') 
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'olympic/SignIn.html', context)

def SignoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
def dashboard(request):
	return render(request, 'olympic/dashboard.html')


def home(request):
    return render(request, 'olympic/index.html', {
        'room_name': "broadcast"
    })

from asgiref.sync import async_to_sync
def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast",
        {
            'type': 'send_notification',
            'message': json.dumps("Notification")
        }
    )
    return HttpResponse("Done")


@login_required(login_url='login')
def newsindex(request):
    url = "https://newsapi.org/v2/everything?q=Football&from=2022-09-11&sortBy=popularity&apiKey=4df0c6021cfe480fbb0e5c5a156459f7"

    football_news = requests.get(url).json()

    article = football_news['articles']
    title = []
    desc = []
    img = []

    for i in range(len(article)):
        f = article[i]
        title.append(f['title'])
        desc.append(f['description'])
        img.append(f['urlToImage'])

    newlist = zip(title, desc, img)
    context = {'newlist': newlist}

    return render(request, 'newsindex.html', context)


def videos(request):
    
    video = Video.objects.all()
    lastvideo = Video.objects.last()
    videofile = lastvideo.videofile if lastvideo else None
    video_comments = Comment.objects.filter(post=video).order_by('-id')
    form = VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()

    context = {'videofile': videofile,
                'form':form, 'video':video, 'comments':video_comments
                }
    return render(request, 'olympic/videos.html', context)


@login_required(login_url='login')
def lvideos(request):
    if not request.user.is_authenticated:
        demo_videos = VideoPost.objects.all().order_by('-id')[:5]
        params = {'videos': demo_videos}
        return render(request, 'welcome.html', params)
    else:
        all_videos = VideoPost.objects.all().order_by('-id')
        params = {'all_videos': all_videos}
        return render(request, 'olympic/lvideos.html', params)


@login_required(login_url='login')
def videos1(request, video_id):
    try:
        video_obj = VideoPost.objects.get(id=video_id)
    except ObjectDoesNotExist:
        return render(request, '404.html')
    try:
        session_obj = User.objects.get(username=request.user.username)
    except:
        messages.warning(request, 'You are not login to watch this video.')
        return redirect('home')

    video_comments = Comment.objects.filter(post=video_obj).order_by('-id')

    if request.user not in video_obj.video_views.all():
        video_obj.video_views.add(request.user)

    is_liked = False
    if session_obj in video_obj.likes.all():
        is_liked = True
    else:
        is_liked = False
    params = {'video':video_obj, 'comments': video_comments, 'is_liked':is_liked}
    return render(request, 'olympic/videos1.html', params)


@login_required(login_url='login')
def videos2(request, video_id):
    try:
        video_obj = VideoPost.objects.get(id=video_id)
    except ObjectDoesNotExist:
        return render(request, '404.html')
    try:
        session_obj = User.objects.get(username=request.user.username)
    except:
        messages.warning(request, 'You are not login to watch this video.')
        return redirect('home')

    video_comments = Comment.objects.filter(post=video_obj).order_by('-id')

    if request.user not in video_obj.video_views.all():
        video_obj.video_views.add(request.user)

    is_liked = False
    if session_obj in video_obj.likes.all():
        is_liked = True
    else:
        is_liked = False
    params = {'video':video_obj, 'comments': video_comments, 'is_liked':is_liked}
    return render(request, 'olympic/football1.html', params)


def add_comment(request):
    if request.method == 'GET':
        video_id = request.GET['video_id']
        comment = request.GET['comment_text']
        video_obj = VideoPost.objects.get(id=video_id)
        session_obj = User.objects.get(username=request.user.username)
        video_comments = Comment.objects.filter(post=video_obj).order_by('-id')
        create_comment = Comment.objects.create(post=video_obj, user=session_obj, comment=comment)
        create_comment.save()

    return JsonResponse({'comment':create_comment.comment, 'count_comments':video_comments.count()})


def add_like(request):
    if request.method == 'GET':
        video_id = request.GET['video_id']
        likes = request.GET['likes']
        video_obj = VideoPost.objects.get(id=video_id)
        session_obj = User.objects.get(username=request.user.username)
        video_likes = VideoPost.objects.filter(post=video_obj).order_by('-id')
        create_likes = VideoPost.objects.create(post=video_obj, user=session_obj, likes=likes)
        create_likes.save()

    return JsonResponse({'likes':create_likes.likes, 'count_likes':video_likes.count()})


def get_noti(request):
    return render(request, 'olympic/football1.html')


@login_required(login_url='login')
def football(request):
    matches = Matches.objects.all()
    context = {'matches': matches}
    return render(request, 'olympic/football1.html', context)

def matches(request):
    matches = Matches.objects.all()
    context = {'matches': matches}
    return render(request, 'olympic/matches.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def user(request):
    context = {}
    return render(request, 'olympic/user.html', context)


@login_required(login_url='login')
def fscoreboard(request, myid, matches=None):
    scoreboard = Football_Scoreboard.objects.filter(matches=myid)
    matches = Matches.objects.all()
    context = {'scoreboard': scoreboard, 'matches': matches}
    return render(request, 'olympic/fscoreboard.html', context)


def PostComment(request, matches=None):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        #postId = request.POST.get('postId')
        matches = Matches.objects.get(id = Matches.id)
        comment = Postcomment(comment=comment, user=user, post=matches)
        comment.save()
        messages.success(request, "Your comment has been posted successfully")

    return redirect(f"/scoreboard/{{matches.id}}")


