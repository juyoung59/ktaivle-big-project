from django.urls import path
from . import views

app_name = 'workerschat'
urlpatterns = [
    path('', views.workerschat, name='workerschat'),
    path('test/', views.test, name='test')
]


# 오류나서 views.chat --> views.workerschat로 바꿧숨다