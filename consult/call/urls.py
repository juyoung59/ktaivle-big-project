from django.urls import path
from . import views

app_name = 'call'
urlpatterns = [
    path('', views.call, name='call'),
    path('test/', views.test, name='test')
]
