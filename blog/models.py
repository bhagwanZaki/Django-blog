from typing import DefaultDict
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    images = models.ImageField(null=True,blank=True,upload_to="images/")
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='blog_posts', blank=True, default=None)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})

    
    def num_likes(self):
        return self.like.count()

Choices = (
    ('Like','Like'),
    ('Unlike','Unlike')
)



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    body = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f'{self.post.title} - {self.user}'

    # def get_absolute_url(self):
    #     return reverse("Comment_detail", kwargs={"pk": self.pk})
