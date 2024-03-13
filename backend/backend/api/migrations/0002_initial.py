# Generated by Django 3.2.3 on 2024-03-13 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribelist',
            name='subscribe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_that_subscribe', to=settings.AUTH_USER_MODEL, verbose_name='Подписка'),
        ),
        migrations.AddField(
            model_name='subscribelist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_sublist', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='shoppinglist',
            name='recepie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_list_user', to='api.recepies', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='shoppinglist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_shopping_list', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='recepingredients',
            name='ingredients',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ingredients', verbose_name='Ингредиент'),
        ),
        migrations.AddField(
            model_name='recepingredients',
            name='recep',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recep_ingred', to='api.recepies', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='recepies',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_recepies', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта'),
        ),
        migrations.AddField(
            model_name='recepies',
            name='favorite',
            field=models.ManyToManyField(through='api.FavoriteList', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recepies',
            name='ingredients',
            field=models.ManyToManyField(through='api.RecepIngredients', to='api.Ingredients'),
        ),
        migrations.AddField(
            model_name='recepies',
            name='tags',
            field=models.ManyToManyField(through='api.TagsRecipe', to='api.Tags'),
        ),
        migrations.AddField(
            model_name='favoritelist',
            name='recepie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_user', to='api.recepies', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='favoritelist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorite', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddConstraint(
            model_name='favoritelist',
            constraint=models.UniqueConstraint(fields=('user', 'recepie'), name='unique_favorite'),
        ),
    ]
