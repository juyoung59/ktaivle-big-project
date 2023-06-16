from django.shortcuts import render
from . import models

# Create your views here.
# def chat(request):
#     return render(request, 'chat.html')

def test(request):
    chat = models.Chat.objects.all()
    return render(request, 'chattest.html', {'chat':chat})

def chat(request):
    return render(request, 'chat.html')
