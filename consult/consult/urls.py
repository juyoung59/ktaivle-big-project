from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def home1(request):
    return render(request, 'home1.html')

urlpatterns = [
    path('', home),
    path('home/', home1),
    path('index/', home),
    path("admin/", admin.site.urls),
    path("accounts/", include('accounts.urls')),
    path("chat/", include('chat.urls')),  
    path('call/', include('call.urls')),
    path('foreign/', include('foreign.urls')),
    path('voice/', include('voice.urls')), 
    path('mypage/', include('mypage.urls')),
    path('workerschat/', include('workerschat.urls')), 
    path('board/', include('board.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('editor/', include('django_summernote.urls')),
    # path('STT/', include('STT.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


#  urls.py에서 오류 난 다음에 수정했을 때 꼭 ctrl + c 눌러서 서버 다시 켜주세용 ~!!!!!!!(필수 ~!!!!!)