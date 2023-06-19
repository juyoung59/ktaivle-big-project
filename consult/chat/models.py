from django.db import models
from accounts.models import User

SATICFACTION = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))

# Create your models here.
class Chat(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey('accounts.User', related_name='customer', on_delete=models.CASCADE)
    counselor = models.ForeignKey('accounts.User', related_name='counselor', on_delete=models.CASCADE)
    consult_text = models.TextField()
    consult_date = models.DateTimeField(auto_now_add=True)
    summary = models.TextField()
    satisfaction = models.CharField(choices=SATICFACTION, max_length=1)
    #########추가
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    
    def last_10_messages(self):
        return Chat.objects.order_by('-timestamp').all()[:10]
