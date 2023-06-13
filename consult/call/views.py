from django.shortcuts import render
from . import models

# Create your views here.
def call(request):
    return render(request, 'call.html')

def test(request):
    call = models.Call.objects.all()
    return render(request, 'calltest.html', {'call':call})