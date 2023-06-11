from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return render(request, 'blog/home.html')

def register(request):
    if request.method == 'GET':
        return render(request, 'blog/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return render(request, 'blog/register.html', {'type': 'danger' ,'message': 'Пароль не совпадает, попробуйте еще раз!'})
        return render(request, 'blog/register.html', {'type': 'success' ,'message': 'Все отлично!'})
        # User.objects.create_user()