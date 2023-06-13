from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    path('', views.chat, name='chat'),
    path('test/', views.test, name='test')
]
