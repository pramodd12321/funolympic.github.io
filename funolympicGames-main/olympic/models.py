from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.utils.timezone import now


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
        

class Matches(models.Model):
    id = models.AutoField(primary_key=True)
    country_A = models.CharField(max_length=300, blank=True)
    symbol_A = models.CharField(max_length=300, blank=True)
    country_B = models.CharField(max_length=300, blank=True)
    symbol_B = models.CharField(max_length=300, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    venue = models.CharField(max_length=300, blank=True)
    total_goal_A = models.IntegerField(null=True)
    total_redcard_A = models.IntegerField(null=True)
    total_yellowcard_A = models.IntegerField(null=True)
    total_goal_B = models.IntegerField(null=True)
    total_redcard_B = models.IntegerField(null=True)
    total_yellowcard_B = models.IntegerField(null=True)

    def __str__(self):
        return self.venue if self.venue else ''
        # return str(self.id) if self.id else ''


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Football_Scoreboard(models.Model):
    myid = models.AutoField(primary_key=True, default=1)
    matches = models.ForeignKey(Matches, on_delete=models.SET_NULL, blank=True, null=True)
    players = models.CharField(max_length=200, null=True)
    goal = models.IntegerField(null=True)
    foul = models.IntegerField(null=True)
    yellow_card = models.IntegerField(null=True)
    red_card = models.IntegerField(null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.players


class Address(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    dateofbirth = models.IntegerField(null=True)
    contact = models.IntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='comment_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title



class Postcomment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Matches, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username
    

class Video(models.Model):
    name= models.CharField(max_length=500)
    videofile= models.FileField(upload_to='videos/%y', null=True, verbose_name="")
    desc = models.TextField(default="This is football section.")
    

    def __str__(self):
        return self.name + ": " + str(self.videofile)


class VideoPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    desc = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='videos/thumbnail/', default='none')
    category = models.CharField(max_length=50, default='none')
    pub_date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes')
    video_views = models.ManyToManyField(User, related_name='video_views')

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post = models.ForeignKey(VideoPost, on_delete=models.CASCADE,related_name='comments')
    comment = models.CharField(max_length=300, default="This section has been commented.")

    def __str__(self):
        return '{} commented: '.format(self.user.username)



