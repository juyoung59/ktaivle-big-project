from django.urls import path
from . import views

app_name = 'voice'
urlpatterns = [
    path('', views.call, name='voice'),
    path('test/', views.test, name='test')
]