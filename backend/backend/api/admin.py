from django.contrib import admin

from .models import Tags, Ingredients, Recepies, RecepIngredients


class RecepIngredientsInLine(admin.TabularInline):
    model = RecepIngredients
    extra = 1


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    pass


@admin.register(Recepies, Ingredients)
class RecepiesAdmin(admin.ModelAdmin):
    inlines = (RecepIngredientsInLine,)
