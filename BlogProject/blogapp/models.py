from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField #import this


    # add this

# Create your models here.







class Post(models.Model):
    status_choices=(('draft','Draft'),('published','Published'))
    title=models.CharField(max_length=100)
    slug=models.SlugField(max_length=264,unique_for_date='publish')
    author=models.ForeignKey(User,related_name='blog_posts',on_delete=models.CASCADE)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=status_choices,default='draft')
    image = models.ImageField(upload_to='images',)
    tags = TaggableManager()
    body=RichTextUploadingField() 


    def get_absolute_url(self):
        return f"/{self.slug}/"
    

   

    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return self.title

    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    parent=models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_on']

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)