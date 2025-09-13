from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import UserRegister
from .models import *


def sign_up_by_django(request) -> HttpResponse:
    """
    Демо-функция для регистрации
    :param request:
    :return:
    """
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
                info['error'] = 'Вы должны быть старше 18 лет'
            elif Buyer.objects.filter(name=username).exists():
                info['error'] = 'Пользователь уже существует'
            else:
                # Создаем Django User
                user = User.objects.create_user(username=username, password=password)
                # Создаем Buyer
                buyer = Buyer.objects.create(
                    user=user,
                    name=username, 
                    balance=balance, 
                    age=age
                )
                # Создаем корзину для покупателя
                Cart.objects.create(buyer=buyer)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('platform')
    else:
        form = UserRegister()
    info['form'] = form
    return render(request, 'registration_page.html', info)


def platform(request) -> HttpResponse:
    """
    Демо-функция для главной страницы
    :param request:
    :return:
    """
    context = {
        'total_games': Game.objects.count(),
        'total_buyers': Buyer.objects.count(),
    }
    return render(request, 'platform.html', context)


def store(request) -> HttpResponse:
    """
    Демо-функция для магазина
    :param request:
    :return:
    """
    games = Game.objects.all()
    context = {
        'games': games,
    }
    return render(request, 'store.html', context)


def game_detail(request, game_id: int) -> HttpResponse:
    """
    Демо-функция для детальной страницы игры
    :param request:
    :param game_id:
    :return:
    """
    game = get_object_or_404(Game, id=game_id)
    context = {
        'game': game,
    }
    return render(request, 'game_detail.html', context)


def cart(request) -> HttpResponse:
    """
    Демо-функция для корзины
    :param request:
    :return:
    """
    # Для демонстрации используем первого покупателя
    # В реальном проекте здесь была бы аутентификация
    buyer = Buyer.objects.first()
    if not buyer:
        messages.warning(request, 'Сначала зарегистрируйтесь')
        return redirect('sign_up')
    
    cart_obj, created = Cart.objects.get_or_create(buyer=buyer)
    if request.method == 'POST':
        action = request.POST.get('action')
        game_id = request.POST.get('game_id')
        if action == 'add' and game_id:
            game = get_object_or_404(Game, id=game_id)
            if cart_obj.add_game(game):
                messages.success(request, f'{game.title} добавлена в корзину')
            else:
                messages.info(request, f'{game.title} уже в корзине')
        elif action == 'remove' and game_id:
            game = get_object_or_404(Game, id=game_id)
            if cart_obj.remove_game(game):
                messages.success(request, f'{game.title} удалена из корзины')
        elif action == 'purchase':
            if cart_obj.purchase_all():
                messages.success(request, 'Покупка успешно завершена!')
            else:
                messages.error(request, 'Недостаточно средств на балансе')
        elif action == 'clear':
            cart_obj.clear()
            messages.info(request, 'Корзина очищена')
        return redirect('cart')
    context = {
        'cart': cart_obj,
        'total_cost': cart_obj.get_total_cost(),
        'buyer': buyer,
    }
    return render(request, 'cart.html', context)


def add_to_cart(request, game_id: int) -> HttpResponse:
    """
    Демо-функция для добавления игры в корзину
    :param request:
    :param game_id:
    :return:
    """
    if request.method == 'POST':
        buyer = Buyer.objects.first()  # Демо-пользователь
        if not buyer:
            return JsonResponse({'success': False, 'message': 'Пользователь не найден'})
        cart_obj, created = Cart.objects.get_or_create(buyer=buyer)
        game = get_object_or_404(Game, id=game_id)
        if cart_obj.add_game(game):
            return JsonResponse({'success': True, 'message': f'{game.title} добавлена в корзину'})
        else:
            return JsonResponse({'success': False, 'message': f'{game.title} уже в корзине'})
    return JsonResponse({'success': False, 'message': 'Неверный запрос'})
