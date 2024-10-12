from django.contrib import admin
from .models import Buyer, Game

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance', 'age')
    search_fields = ('name',)
    list_filter = ('balance', 'age')

@admin.register(Game)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'cost', 'size')
    #fields = ['title', ('cost', 'size'), 'description',]
    search_fields = ('title',)
    list_filter = ('cost', 'size')
    fieldsets = (
        ('INFO', {
            'fields':
                ('title', 'cost', 'size')
        }),
        ('ADD', {
            'fields':
                ('description',)
        })
    )