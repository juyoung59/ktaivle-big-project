# from django.shortcuts import render
# from .googlespeech import Gspeech
# import time
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.template import loader
# # Create your views here.

# def STT(request): #접속 시 첫 화면
#     return render(request, 'button.html')

# @csrf_exempt
# def apic(request): #api 호출 함수
#     gsp = Gspeech()
#     while True:
#             # 음성 인식 될때까지 대기 한다.
#         stt = gsp.getText()
#         if stt is None:
#             break
#         print(stt)
#         time.sleep(0.01)
#         break

#     return HttpResponse(str(stt))