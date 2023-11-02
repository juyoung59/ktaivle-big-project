from django.shortcuts import render
from . import models

# Create your views here.
def workerschat(request):
    return render(request, 'workerschat.html')



def test(request):
    workerschat = models.Workerschat.objects.all()
    return render(request, 'workerschattest.html', {'workerschat':workerschat})


