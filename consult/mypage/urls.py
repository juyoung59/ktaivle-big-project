from django.urls import path
from . import views

app_name = 'mypage'
urlpatterns = [
    path('', views.mypage, name='mypage'),
    path('update/', views.update, name='update'),
    path('chatdetail/<cpk>', views.chatdetail, name='chatdetail'),
    path('calldetail/<cpk>', views.calldetail, name='calldetail'),
]
