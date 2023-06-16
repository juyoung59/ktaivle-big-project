from django.urls import path
from . import views

app_name = 'survey' 
urlpatterns = [
    path('', views.submit, name='submit'),
    path('submitted/', views.submitted, name='submitted'),
]
