import os
import sys
import django
from datetime import date

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GameStore.settings')
django.setup()

from task1.models import Game, Buyer, Cart
from django.contrib.auth.models import User

# Создаем тестовые игры
games_data = [
    {
        'title': 'Cyberpunk 2077',
        'cost': 1999.00,
        'size': 70.5,
        'description': 'Открытый мир в жанре киберпанк с захватывающим сюжетом и множеством возможностей для исследования.',
        'age_limited': True,
        'min_age': 18,
        'genre': 'RPG',
        'developer': 'CD Projekt RED',
        'release_date': date(2020, 12, 10)
    },
    {
        'title': 'The Witcher 3: Wild Hunt',
        'cost': 1299.00,
        'size': 50.0,
        'description': 'Эпическая RPG о ведьмаке Геральте в фэнтезийном мире. Одна из лучших игр всех времен.',
        'age_limited': True,
        'min_age': 18,
        'genre': 'RPG',
        'developer': 'CD Projekt RED',
        'release_date': date(2015, 5, 19)
    },
    {
        'title': 'Minecraft',
        'cost': 899.00,
        'size': 1.0,
        'description': 'Песочница для творчества, где можно строить, исследовать и выживать в бесконечном мире.',
        'age_limited': False,
        'min_age': 7,
        'genre': 'Песочница',
        'developer': 'Mojang Studios',
        'release_date': date(2011, 11, 18)
    },
    {
        'title': 'Among Us',
        'cost': 199.00,
        'size': 0.5,
        'description': 'Мультиплеерная игра на выживание, где нужно найти предателя среди команды.',
        'age_limited': False,
        'min_age': 10,
        'genre': 'Парти',
        'developer': 'InnerSloth',
        'release_date': date(2018, 6, 15)
    },
    {
        'title': 'Valorant',
        'cost': 0.00,
        'size': 25.0,
        'description': 'Тактический шутер от первого лица с элементами героев. Бесплатная игра с внутриигровыми покупками.',
        'age_limited': True,
        'min_age': 16,
        'genre': 'FPS',
        'developer': 'Riot Games',
        'release_date': date(2020, 6, 2)
    },
    {
        'title': 'Stardew Valley',
        'cost': 599.00,
        'size': 0.5,
        'description': 'Уютная фермерская симуляция с элементами RPG. Идеальная игра для расслабления.',
        'age_limited': False,
        'min_age': 10,
        'genre': 'Симулятор',
        'developer': 'ConcernedApe',
        'release_date': date(2016, 2, 26)
    }
]

# Создаем тестового покупателя
user = User.objects.create_user(username='testuser', password='testpass123')
buyer = Buyer.objects.create(
    user=user,
    name='Тестовый Покупатель',
    balance=5000.00,
    age=25
)
cart = Cart.objects.create(buyer=buyer)

# Создаем игры
for game_data in games_data:
    game = Game.objects.create(**game_data)
    print(f"Создана игра: {game.title}")

print(f"\nСоздан покупатель: {buyer.name} с балансом {buyer.balance} ₽")
print("Тестовые данные успешно добавлены!")
