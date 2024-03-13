from django.contrib import admin

from .models import (Tags, Ingredients, Recepies, RecepIngredients,
                     TagsRecipe, FavoriteList, ShoppingList, SubscribeList)


class RecepIngredientsInLine(admin.TabularInline):
    model = RecepIngredients
    extra = 1
    min_num = 1


@admin.register(Tags, RecepIngredients, TagsRecipe,
                FavoriteList, ShoppingList, SubscribeList)
class TagsAdmin(admin.ModelAdmin):
    pass


@admin.register(Recepies, Ingredients)
class RecepiesAdmin(admin.ModelAdmin):
    inlines = (RecepIngredientsInLine,)
