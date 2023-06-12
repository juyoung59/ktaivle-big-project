from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.forms import LoginForm, SignUpForm
from django.core.mail.message import EmailMessage
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.http import HttpResponse

User = get_user_model()

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
    
        if form.is_valid():
            user = form.save()
            return redirect('index')
        else:
            messages.error(request, '회원가입에 실패했습니다.')
            print(form.errors)
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated: 
        return redirect('index') 
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.warning(request, "로그인 정보가 올바르지 않습니다.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def resetpw(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.error(request, '회원가입에 실패했습니다.')
    else:
        form = UserCreationForm()
    
    return render(request, 'resetpw.html', {'form': form})


def send_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse('사용자를 찾을 수 없습니다.')
        
        
        subject = "비밀번호 재설정하기"
        from_email = "ktaivle14@gmail.com"
        message = "비밀번호 재설정 링크 테스트"
        email_message = EmailMessage(subject=subject, body=message, to=[user.email], from_email=from_email)
        email_message.send()
        return HttpResponse('이메일 전송 완료')
    else:
        return HttpResponse('잘못된 요청입니다.')