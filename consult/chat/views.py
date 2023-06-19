from django.shortcuts import render
from . import models

import openai #추가(0619)
openai.api_key = "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" #추가(0619) 프로젝트 끝나고 API키 삭제 예정
from django.http import JsonResponse#추가(0619)

import json

# Create your views here.
# def chat(request):
#     return render(request, 'chat.html')


def test(request):
    chat = models.Chat.objects.all()
    return render(request, 'chat/chattest.html', {'chat':chat})


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
    # 밑에 코드 실행 시 주의문구 제거 가능 그러나 여러 육두문자 시험해본 결과 다른형태 경고문구 존재함 좀 더 찾아볼 필요 있음
    # result=response["choices"][0]["message"]["content"]
    # if "Note:" in result:
    #     result=result.split("Note:",1)[0].strip()
    # return JsonResponse({"result":result},json_dumps_params={'ensure_ascii': False})
    #return response["choices"][0]["message"]["content"]
    return JsonResponse({"result":response["choices"][0]["message"]["content"]},json_dumps_params={'ensure_ascii': False})

def test2(request):
    return render(request, 'chat/test2.html')
################################################################33




def chat(request):
    return render(request, 'chat/chat_t.html')

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})