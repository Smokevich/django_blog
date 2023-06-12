from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db import IntegrityError
from .models import UserProfile

# Create your views here.
def home(request):
    return render(request, 'blog/home.html')


@login_required
def my_account(request):
    return render(request, 'blog/account.html')


def new_post(request):
    if request.method == 'GET':
        return render(request, 'blog/new_post.html')
    elif request.method == 'POST':
        pass


def register(request):
    if request.method == 'GET':
        return render(request, 'blog/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.add_message(request, messages.WARNING, 'Пароль не совпадает, попробуйте еще раз!')
            return render(request, 'blog/register.html')
        try:
            user = User.objects.create_user(username, email, password1)
            UserProfile.objects.create(user=user)
            messages.add_message(request, messages.SUCCESS, 'Вы успешно зарегистрированы!')
            login(request, user)
            return redirect('home')
        except IntegrityError:
            messages.add_message(request, messages.WARNING, 'Данный пользователь уже существует!')
            return render(request, 'blog/register.html')


def login_user(request):
    if request.method == 'GET':
        return HttpResponseForbidden()
    elif request.method == 'POST':
        user = authenticate(request, 
                            username=request.POST.get('username'), 
                            password=request.POST.get('password')
                            )
        if user:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Вы успешно вошли в аккаунт!')
            return redirect('home')
        else:
            messages.add_message(request, messages.WARNING, 'Вы ввели неверный логин или пароль!')
            return redirect('home')
        

@login_required    
def logout_user(request):
    logout(request)
    return redirect('home')