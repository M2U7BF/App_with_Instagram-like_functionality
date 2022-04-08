from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    # file will be uploaded to MEDIA_ROOT / uploads
    upload_img = models.ImageField(upload_to = 'images',verbose_name='投稿画像')
    posted_at = models.DateTimeField(help_text="投稿日",auto_now_add=True,verbose_name='投稿日')
    text = models.CharField(max_length=255,verbose_name='本文')
    good = models.IntegerField(default=0,verbose_name='いいねの数')

    def __str__(self):
        return self.text[:10]

class Comment(models.Model):
    subject = models.ForeignKey(Post, on_delete=models.CASCADE,verbose_name='コメント投稿先')
    posted_at = models.DateTimeField(help_text="投稿日",auto_now_add=True,primary_key=True,verbose_name='コメント投稿日')
    text = models.CharField(max_length=255,verbose_name='本文')
    good = models.IntegerField(default=0,verbose_name='いいねの数')

    def __str__(self):
        return self.text[:10]
    