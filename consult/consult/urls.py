from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def i18ntest(request):
    return render(request, 'i18ntest.html')


urlpatterns = [
    path('', index),
    path("admin/", admin.site.urls),
    path("accounts/", include('accounts.urls')),
    path("chat/", include('chat.urls')),  
    path('i18n/', include('django.conf.urls.i18n')),
    path('call/', include('call.urls')),
    path('foreign/', include('foreign.urls')),
    path('voice/', include('voice.urls')), 
    path('mypage/', include('mypage.urls')),
]




#  urls.py에서 오류 난 다음에 수정했을 때 꼭 ctrl + c 눌러서 서버 다시 켜주세용 ~!!!!!!!(필수 ~!!!!!)