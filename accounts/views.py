from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'POST': # POST 요청일 경우 로그인 기능 수행
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) # 장고 제공하는 사옹자 확인 함수
        if user is not None:
            auth_login(request, user) # 장고에서 제공하는 로그인 처리 함수
            return redirect('home')
        else:
            context = {'error': '아이디 또는 비밀번호가 잘못되었습니다.'}
            return render(request, 'accounts/login.html', context)
    else:
        # GET 요청일 경우 로그인 HTML 응답
        return render(request, 'accounts/login.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # if len(username) < 5:
        #     pass
        if password1 == password2:
            User.objects.create_user(
                username = username,
                email = email,
                password = password1
            )
        else:
            context = {
                'error': '비밀번호와 비밀번호 확인이 일치하지 않습니다.'
            }
            return render(request, 'accounts/signup.html', context)
        return redirect('home')
    # 사용자 생성 폼 응답
    else:
        return render(request, 'accounts/signup.html')