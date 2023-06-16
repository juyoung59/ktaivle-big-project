from django.shortcuts import render,redirect
from accounts.models import User
from django.utils import timezone
# from .models import Voice

def test(request):
    username = None
    counselor_list = User.objects.filter(member_type='Counselor')
    if request.user.is_authenticated:  # 사용자가 인증된 경우에만 사용자 이름 가져오기
        username = request.user.username
    #     counselor_list = User.objects.all()
    
    context = {
        'username': username,
        'counselor_list': counselor_list
    }
    return render(request, 'voice.html', context)

def test1(request):
    username = None
    counselor_list = User.objects.filter(member_type='Counselor')
    if request.user.is_authenticated:  # 사용자가 인증된 경우에만 사용자 이름 가져오기
        username = request.user.username
    #     counselor_list = User.objects.all()
    
    context = {
        'username': username,
        'counselor_list': counselor_list
    }
    return render(request, 'voice_test.html', context)


# def call_view(request):
#     if request.method == 'POST':
#         action = request.POST.get('action')

#         if action == 'start':
#             # 전화 시작 시간을 저장
#             start_time = timezone.now()
#             request.session['start_time'] = start_time
#         elif action == 'stop':
#             # 전화 종료 시간을 저장
#             end_time = timezone.now()
#             start_time = request.session.pop('start_time', None)

#             if start_time:
#                 # 시작 시간과 종료 시간을 DB에 저장
#                 call = Voice(start_time=start_time, end_time=end_time)
#                 call.save()

#         return redirect('call_complete')

#     return render(request, 'voice.html')

# def call_complete(request):
#     return render(request, 'home.html')


