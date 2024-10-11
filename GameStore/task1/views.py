from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegister
from .models import *

# Create your views here.

def sign_up_by_django(request):
    info = {}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']
            balance = form.cleaned_data['balance']

            if password != repeat_password:
                info['error'] = 'Пароли не совпадают'
            elif age < 18:
                info['error'] = 'Вы должны быть старше 18'
            elif Buyer.objects.filter(name=username).exists():
                info['error'] = 'Пользователь уже существует'
            else:
                Buyer.objects.create(name=username, balance=balance, age=age)
                return HttpResponse(f'Приветствуем, {username}!')

    else:
        form = UserRegister()
    info['form'] = form

    return render(request, 'registration_page.html', info)

# def sign_up_by_html(request):
#     info ={}
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         repeat_password = request.POST.get('repeat_password')
#         age = request.POST.get('age')
#         try:
#             age = int(age)
#             if password != repeat_password:
#                 info['error'] = 'Пароли не совпадают'
#             elif age < 18:
#                 info['error'] = 'Вы должны быть старше 18'
#             elif username in users:
#                 info['error'] = 'Пользователь уже существует'
#             else:
#                 return HttpResponse(f'Приветствуем, {username}!')
#         except ValueError:
#             info['error'] = 'Введите корректный возраст'
#     form = UserRegister()
#     info['form'] = form
#     return render(request, 'registration_page.html', info)



def store(request):
    Games = Game.objects.all()
    context = {
        'Games': Games,
    }
    return render(request, 'store.html', context)

def cart(request):
    return render(request, 'cart.html')

def platform(request):
    return render(request, 'platform.html')
