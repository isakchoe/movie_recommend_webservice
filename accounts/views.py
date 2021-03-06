from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model, update_session_auth_hash

from .forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()


@require_http_methods(['GET', 'POST'])
def signup(request):  # User model CREATE
    # 인증된 사용자는 pass
    if request.user.is_authenticated:
        return redirect('movies:home')

    # Create User Instance
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login => cookie & session settings
            auth_login(request, user)
            return redirect('movies:home')
    else:
        form = CustomUserCreationForm()
        
    context = {'form': form,}
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def update(request):
    # 회원정보 수정은, 타인이 아닌 본인에 의해서만 가능
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = CustomUserChangeForm(request.POST, instance=user)
            if form.is_valid():
                user = form.save()
                return redirect('movies:home')
        else:
            form = CustomUserChangeForm(instance=user)
        
        context = {
            'form': form
        }
    return render(request, 'accounts/update.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('movies:home')
    else:
        form = PasswordChangeForm(user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)


@require_POST
def delete(request):
    # 회원정보 삭제는, 타인이 아닌 본인에 의해서만 가능
    user = request.user
    if user.is_authenticated:
        user.delete()
    return redirect('movies:home')


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:home')

    if request.method == 'POST':
        # AuthenticationForm => 일반 Form
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():  # authenticate(id, pw) => 맞으면, user 객체를 반환
            user = form.get_user()
            auth_login(request, user)  # auth_login() => session & cookie 세팅
            return redirect(request.GET.get('next') or 'movies:home')
    else:
        form = AuthenticationForm()

    context = {'form': form,}
    return render(request, 'accounts/login.html', context)
    

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)  # auth_logout => session, cookie 날리기
    return redirect('movies:home')

