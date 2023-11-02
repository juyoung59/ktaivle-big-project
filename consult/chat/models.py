from django.db import models
from accounts.models import User

# Create your models here.
class Chat(models.Model):
    id = models.BigAutoField(primary_key=True)
    
    user = models.ForeignKey('accounts.User', related_name='chat_user', on_delete=models.CASCADE)
    contact = models.ForeignKey('Contact', related_name='chat_contact', on_delete=models.CASCADE)
    message = models.ForeignKey('Message', related_name='chat_messages', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    
    @classmethod
    def last_10_messages(self):
        return Chat.objects.order_by('-timestamp').all()[:10]
    
    # def last_10_messages(self, caht_id):
    #     return Message.objects.filter(chat_id=chat_id).order_by('created_at')[:10]
    
class Contact(models.Model):
    user = models.ForeignKey('accounts.User', related_name='contact_user', on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', related_name='contact_chat', on_delete=models.CASCADE)
    
class Message(models.Model):
    user = models.ForeignKey('accounts.User', related_name='message_user', on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', related_name='message_chat', on_delete=models.CASCADE, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
