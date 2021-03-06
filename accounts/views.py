from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from works.models import PlaceSelected

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
                'error': 'please check your password again'
            }
            return render(request, 'accounts/signup.html', context)
        return redirect('home')
    # 사용자 생성 폼 응답
    else:
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST': # POST 요청일 경우 로그인 기능 수행
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) # 장고 제공하는 사옹자 확인 함수
        if user is not None:
            auth_login(request, user) # 장고에서 제공하는 로그인 처리 함수
            # context = {
            #     'username': username
            # }
            # return render(request, 'home/home.html', context)
            return redirect('home')
        else:
            context = {'error': 'invalid ID and/or PASSWORD'}
            return render(request, 'accounts/login.html', context)
    else:
        # GET 요청일 경우 로그인 HTML 응답
        return render(request, 'accounts/login.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')

@login_required
def history(request):
    history_all = PlaceSelected.objects.filter(user=request.user)
    context = {
        'history_all': history_all
    }
    return render(request, 'accounts/history.html', context)

@login_required
def delete(request):
    history_all = PlaceSelected.objects.filter(user=request.user)
    if request.method == 'POST':
        history_all.delete()
        return redirect('accounts:history')