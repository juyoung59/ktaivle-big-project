from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    path('', views.chat, name='chat'),
    path('test/', views.test, name='test'),
    #(0619 테스트용)########################
    path("test2/",views.test2,name='test2'),
    path("translater/",views.translater,name='translater'),
    ########################################
    path("<str:room_name>/", views.room, name="room"),   
]
