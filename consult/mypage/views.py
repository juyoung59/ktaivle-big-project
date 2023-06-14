from django.shortcuts import render
from accounts.models import User
from chat.models import Chat
from call.models import Call

# Create your views here.
def mypage(request):
    if request.user.member_type == 'Customer':
        chats = Chat.objects.filter(customer=request.user.id)
        calls = Call.objects.filter(customer=request.user.id)
    elif request.user.member_type == 'Counselor':
        chats = Chat.objects.filter(counselor=request.user.id)
        calls = Call.objects.filter(counselor=request.user.id)
        
    return render(request, 'mypage.html', {'chats':chats, 'calls':calls})

def update(request):
    return render(request, 'mypage_update.html')

def chatdetail(request, cpk):
    url = 'chatdetail' + '/' + cpk
    consult_type = 'chat'
    consult = Chat.objects.get(id=cpk)
        
    return render(request, 'mypage_detail.html', {'consult_type':consult_type, 'consult':consult, 'url':url})

def calldetail(request, cpk):
    url = 'calldetail' + '/' + cpk
    consult_type = 'call'
    consult = Call.objects.get(id=cpk)
        
    return render(request, 'mypage_detail.html', {'consult_type':consult_type, 'consult':consult, 'url':url})