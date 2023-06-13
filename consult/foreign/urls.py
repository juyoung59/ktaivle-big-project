from django.urls import path
from . import views

app_name = 'foreign'
urlpatterns = [
    path('', views.foreign, name='foreign'),
]
