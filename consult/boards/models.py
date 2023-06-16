from django.db import models
from accounts.models import User

CATEGORY = (('FAQ', 'FAQ'), ('Inquiry', 'Inquiry'))

# Create your models here.
class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64)
    detail = models.TextField(default='', null=True)
    writer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    category =  models.CharField(choices=CATEGORY, max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    
class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commenter = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    