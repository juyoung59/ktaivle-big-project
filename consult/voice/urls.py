from django.urls import path
from . import views

app_name = 'voice'
urlpatterns = [
    path('', views.test, name='test'),
    # path('', views.call_view, name='call_view'),
    path('voicetest/', views.test1, name='test1'),
]