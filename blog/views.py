from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.db import IntegrityError
from django.core.mail import send_mail
from django.core.paginator import Paginator
from .models import UserProfile, Post, Tag, Promotion, HistoryViews, RatingPost, RatingAuthor
from .forms import PostForm, SettingForm
from random import choice

# Create your views here.
def home(request):
    posts = Post.objects.filter(is_active=True).order_by('-created_at')[:11]
    promotionValuesId = Promotion.objects.filter(is_enabled=True)
    if promotionValuesId:
        promotionRandomId = choice(promotionValuesId.values_list('id', flat=True))
        promotion = Promotion.objects.get(id=promotionRandomId)
    else:
        promotion = None
    context = {'posts': posts, 'promotion': promotion}
    return render(request, 'blog/home.html', context)

def get_sidebar():
    postRating = RatingPost.objects.order_by('-count_views').all()[:10]
    authorRating = RatingAuthor.objects.order_by('-count_views').all()[:10]
    return {'postRating': postRating, 'authorRating': authorRating}



def all_posts(request):
    posts = Post.objects.filter(is_active=True).order_by('-created_at')
    paginator = Paginator(posts, 2)
    pageNumber = request.GET.get('page')
    pageObject  = paginator.get_page(pageNumber)
    sidebar = get_sidebar()
    context = {'posts': pageObject, 'postRating': sidebar['postRating'], 'authorRating': sidebar['authorRating']}

    return render(request, 'blog/all_posts.html', context)


def all_users(request):
    users = User.objects.filter(is_active=True)
    sidebar = get_sidebar()
    context = {'users': users, 'postRating': sidebar['postRating'], 'authorRating': sidebar['authorRating']}
    return render(request, 'blog/all_users.html', context)


def search_page(request):
    searchWord = request.POST.get('search')
    searchPost = Post.objects.filter(name__contains=searchWord)
    searchUser = User.objects.filter(username__contains=searchWord)
    sidebar = get_sidebar()
    context = {'resultSearch': searchWord, 'resultPost': searchPost, 'resultUser': searchUser, 'postRating': sidebar['postRating'], 'authorRating': sidebar['authorRating']}
    return render(request, 'blog/search.html', context)


def account(request, id):
    user = get_object_or_404(User, id=id)
    posts = Post.objects.filter(author_id=id)
    count_posts = Post.objects.filter(author_id=id).count()
    if not user.is_active:
        return handler404(request)
    sidebar = get_sidebar()
    context = {'user': user, 'posts': posts, 'count_posts': count_posts, 'postRating': sidebar['postRating'], 'authorRating': sidebar['authorRating']}
    return render(request, 'blog/account.html', context)

@login_required
def settings(request):
    if request.method == 'GET':
        return render(request, 'blog/settings.html', get_sidebar())
    if request.method == 'POST':
        password = request.POST.get('password')
        if check_password(password, request.user.password):
            user = User.objects.get(id=request.user.id)
            button = request.POST.get('button')
            if button == 'delete':
                user.is_active = False
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Аккаунт успешно удален!')
                return redirect('home')
            elif button == 'change':
                user.first_name = request.POST.get('first-name')
                user.last_name = request.POST.get('last-name')
                if len(request.POST.get('password1')) > 5:
                    if request.POST.get('password1') != request.POST.get('password2'):
                        messages.add_message(request, messages.ERROR, 'Пароль не совпадает')
                    else:
                        user.set_password(request.POST.get('password1'))
                    
                profile = UserProfile.objects.get(user_id=request.user.id)
                if request.FILES.get('image'):
                    if 'image' in request.FILES['image'].content_type:
                        profile.avatar = request.FILES.get('avatar')
                        profile.save()
                    else:
                        messages.add_message(request, messages.ERROR, 'Данный формат изображения не поддерживается, попробуйте другой.')
                user.save()
                if not messages.get_messages(request):
                    messages.add_message(request, messages.SUCCESS, 'Данные успешно изменены!')

            # messages.add_message(request, messages.SUCCESS, 'Пароль совпадает!')
        else: 
            messages.add_message(request, messages.ERROR, 'Пароль не совпадает!')
        return redirect('settings')



def support(request):
    if request.method == 'GET':
        return render(request, 'blog/support.html', get_sidebar())
    elif request.method == 'POST':
        address = ['swapper12@gmail.com']
        data = {'email': request.POST.get('email'),
                'subject': request.POST.get('subject'),
                'text': request.POST.get('text'),}
        
        if not data['email']:
            messages.add_message(request, messages.ERROR, 'Вы ввели некорректную почту!')
            return render(request, 'blog/support.html')
        if not data['subject']:
            messages.add_message(request, messages.ERROR, 'Вы ввели некорректную тему!')
            return render(request, 'blog/support.html')
        if not data['text']:
            messages.add_message(request, messages.ERROR, 'Вы не написали текст сообщения!')
            return render(request, 'blog/support.html')
        try:
            send_mail(data['subject'], data['text'], data['email'], address, False)
            messages.add_message(request, messages.SUCCESS, 'Сообщение успешно отправлено! В ближайшее время вам ответят.')
        except ConnectionRefusedError:
            messages.add_message(request, messages.ERROR, 'Не удалось отправить сообщение из-за ошибки на сервере почты.')
        except:
            messages.add_message(request, messages.ERROR, 'Неизветсная ошибка! Попробуйте позже.')
        finally:
            return render(request, 'blog/support.html')

@login_required
def new_post(request):
    if request.method == 'GET':
        return render(request, 'blog/new_post.html', get_sidebar())
    elif request.method == 'POST':
        tags = request.POST.get('tags').strip().title()
        if not Tag.objects.filter(name=tags):
            Tag.objects.create(name=tags)
        tag = Tag.objects.get(name=tags)
        try:
            result = PostForm(request.POST, request.FILES).save(commit=False)
            result.author_id = request.user
            result.tag_id = tag
            result.is_active = True
            result.save()        
            messages.add_message(request, messages.SUCCESS, 'Пост успешно создан!')
            return render(request, 'blog/new_post.html')
        except ValueError:
            messages.add_message(request, messages.ERROR, 'Максимальная длина одного из полей была больше допустимого лимита.</br>Попробуйте сократить текст.')
        except:
            messages.add_message(request, messages.ERROR, 'Неизвестная ошибка.')
        finally:
            return render(request, 'blog/new_post.html')
        

@login_required
def edit_post(request, id_post):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=id_post)
        if post.author_id != request.user:
            return handler404(request)
        sidebar = get_sidebar()
        context = {'post': post, 'postRating': sidebar['postRating'], 'authorRating': sidebar['authorRating']}
        return render(request, 'blog/edit_post.html', context)
    elif request.method == 'POST':
        method = request.POST.get('button')
        post = Post.objects.get(id=id_post)
        if post.author_id != request.user:
            return HttpResponseNotFound
        if method == 'delete':
            post.delete()
            messages.add_message(request, messages.SUCCESS, 'Пост успешно удален!')
            return redirect('account', request.user)
        elif method == 'change':
            tags = request.POST.get('tags')
            tag = Tag.objects.get(name=tags.title())
            if not tag:
                Tag.objects.create(name=tags.title())
                tag = Tag.objects.get(name=tags.title())
            result = PostForm(request.POST, request.FILES, instance=post).save(commit=False)
            result.author_id = request.user
            result.tag_id = tag
            result.save()
            messages.add_message(request, messages.SUCCESS, 'Пост успешно изменен!')
            return redirect('post-page', id_post)


def page_post(request, id_post):
    post = get_object_or_404(Post, id=id_post)
    if post.is_active:
        HistoryViews.objects.create(user=request.user, post_id=post, author_id=post.author_id)
        if not RatingPost.objects.filter(id=post):
            RatingPost.objects.create(id=post)
        statsPost = RatingPost.objects.get(id=post)
        statsPost.count_views += 1
        statsPost.save()

        if not RatingAuthor.objects.filter(id=post.author_id):
            RatingAuthor.objects.create(id=post.author_id)
        statsAuthor = RatingAuthor.objects.get(id=post.author_id)
        statsAuthor.count_views += 1
        statsAuthor.save()

        sidebar = get_sidebar()
        context = {'post': post, 'postRating': sidebar['postRating'], 'authorRating': sidebar['authorRating']}
        return render(request, 'blog/post.html', context)
    else:
        return handler404(request)

def register(request):
    if request.method == 'GET':
        return render(request, 'blog/register.html', get_sidebar())
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.add_message(request, messages.ERROR, 'Пароль не совпадает, попробуйте еще раз!')
            return render(request, 'blog/register.html')
        try:
            user = User.objects.create_user(username, email, password1)
            UserProfile.objects.create(user=user)
            messages.add_message(request, messages.SUCCESS, 'Вы успешно зарегистрированы!')
            login(request, user)
            return redirect('home')
        except IntegrityError:
            messages.add_message(request, messages.ERROR, 'Данный пользователь уже существует!')
            return render(request, 'blog/register.html')


def login_user(request):
    if request.method == 'GET':
        return handler404(request)
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
            messages.add_message(request, messages.ERROR, 'Вы ввели неверный логин или пароль!')
            return redirect('home')
        

@login_required    
def logout_user(request):
    logout(request)
    return redirect('home')

def handler404(request):
    response = render(request, 'blog/404.html',)
    response.status_code = 404
    return response