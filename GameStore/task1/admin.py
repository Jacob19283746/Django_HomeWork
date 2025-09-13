from django.contrib import admin
from .models import Buyer, Game, Cart


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'balance', 'created_at')
    list_filter = ('age', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'developer', 'genre', 'cost', 'min_age', 'created_at')
    list_filter = ('genre', 'age_limited', 'developer', 'created_at')
    search_fields = ('title', 'developer', 'description')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'developer', 'genre')
        }),
        ('Цена и размер', {
            'fields': ('cost', 'size')
        }),
        ('Возрастные ограничения', {
            'fields': ('age_limited', 'min_age')
        }),
        ('Дополнительно', {
            'fields': ('release_date', 'image_url', 'created_at')
        }),
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'get_games_count', 'get_total_cost', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    def get_games_count(self, obj):
        return obj.games.count()
    get_games_count.short_description = 'Количество игр'
    
    def get_total_cost(self, obj):
        return f"{obj.get_total_cost()} ₽"
    get_total_cost.short_description = 'Общая стоимость'
