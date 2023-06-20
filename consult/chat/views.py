from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from . import models
from accounts.models import User
from .models import Chat, Contact, Message
from django.utils.safestring import mark_safe


import openai #추가(0619)
from django.http import JsonResponse#추가(0619)
import json

# Create your views here.
openai.api_key = "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" #추가(0619) 프로젝트 끝나고 API키 삭제 예정

#######(0619테스트용)####################
def translater(request):
    data = json.loads(request.body)
    language = data["language"]
    text = data["text"]

    prompt = f"{text}\n\nTranslate this sentence into {language}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "you are a translater"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=500,
    )
    
    result=response["choices"][0]["message"]["content"]
    if "Note:" in result:
        result=result.split("Note:",1)[0].strip()
    return JsonResponse({"result":result},json_dumps_params={'ensure_ascii': False})
    #return JsonResponse({"result":response["choices"][0]["message"]["content"]},json_dumps_params={'ensure_ascii': False})

def test2(request):
    return render(request, 'chat/test2.html')
################################################################33
###### 코드 정리 하면서 진행 부탁 드립니다 #######



####  조별 코칭 전에 이거 주석해제 하고 밑에 있는 chat 주석처리 해주세요 ####

# def chat(request):
#     return render(request, 'chat/chat.html')

@login_required
def chat(request):
    if request.user.is_authenticated:
        # 채팅방 목록
        chat_rooms = Contact.objects.filter(user=request.user)
        print(chat_rooms)
        
        return render(request, 'chat/index.html')
    else:
        return redirect('accounts:login')

@login_required
def room(request, room_name):
    try:
        return render(request, "chat/roomtest.html", {"room_name": mark_safe(json.dumps(room_name)),
                                                  'username': request.user.username})
    except:
        return redirect('chat:chat')

def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]

def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Contact, user=user)

def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)