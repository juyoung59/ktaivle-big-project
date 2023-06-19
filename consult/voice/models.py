from django.db import models
from accounts.models import User

# Create your models here.

class Voice(models.Model):
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'outgoing_calls')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_calls')
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    duration = models.DurationField(blank=True, null=True)
    
    # def save(self, *args, **kwargs):
    #     if self.start_time and self.end_time:
    #         self.duration = self.end_time - self.start_time
    #     super().save(*args, **kwargs)
        
    # def __str__(self):
    #     return f"Call from {self.caller.username} to {self.receiver.username}"