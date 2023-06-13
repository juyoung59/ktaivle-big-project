from django.shortcuts import render
from accounts.models import User
from chat.models import Chat
from call.models import Call

# Create your views here.
def mypage(request):
    return render(request, 'mypage.html')

# def mypage(request):
#     if request.user.member_type == 'Customer':
#         chats = Chat.objects.filter(customer=request.user.id)
#         calls = Call.objects.filter(customer=request.user.id)
#         print(chats)
#     elif request.user.member_type == 'Counselor':
#         chats = Chat.objects.filter(counselor=request.user.id)
#         calls = Call.objects.filter(counselor=request.user.id)
#         print(chats)
        
#     return render(request, 'mypage.html', {'chats':chats, 'calls':calls})