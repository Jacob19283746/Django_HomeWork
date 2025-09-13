from django.db import models
from django.contrib.auth.models import User

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def can_afford(self, amount):
        """
        Проверка, хватает ли средств
        :param amount:
        :return:
        """
        return self.balance >= amount

    def purchase_game(self, game):
        """
        Покупка игры
        :param game:
        :return:
        """
        if self.can_afford(game.cost):
            self.balance -= game.cost
            self.save()
            return True
        return False


class Game(models.Model):
    title = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Размер в ГБ")
    description = models.TextField()
    age_limited = models.BooleanField(default=False)
    min_age = models.IntegerField(default=0)
    genre = models.CharField(max_length=50, default="Не указан")
    developer = models.CharField(max_length=100, default="Неизвестно")
    release_date = models.DateField(null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    buyers = models.ManyToManyField(Buyer, related_name='owned_games', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Cart(models.Model):
    buyer = models.OneToOneField(Buyer, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Корзина {self.buyer.name}"

    def get_total_cost(self):
        """
        Получение общей стоимости игр в корзине
        :return:
        """
        return sum(game.cost for game in self.games.all())

    def add_game(self, game):
        """
        Добавление игры в корзину
        :param game:
        :return:
        """
        if game not in self.games.all():
            self.games.add(game)
            return True
        return False

    def remove_game(self, game):
        """
        Удаление игры из корзины
        :param game: Игра
        :return:
        """
        if game in self.games.all():
            self.games.remove(game)
            return True
        return False

    def clear(self):
        """
        Очистка корзины
        :return:
        """
        self.games.clear()

    def purchase_all(self):
        """
        Покупка всех игр в корзине
        :return:
        """
        total_cost = self.get_total_cost()
        if self.buyer.can_afford(total_cost):
            for game in self.games.all():
                self.buyer.owned_games.add(game)
            self.buyer.balance -= total_cost
            self.buyer.save()
            self.clear()
            return True
        return False
