from django.db import models
from accounts.models import User

# Create your models here.

class Voice(models.Model):
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'outgoing_calls')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_calls')
    
