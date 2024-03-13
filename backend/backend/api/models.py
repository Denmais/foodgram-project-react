from django.db import models
from users.models import UserModel
from api.validators import validate_color
from django.core.validators import MinValueValidator
import api.constants as const


class Tags(models.Model):
    """Модель тегов."""
    name = models.CharField(max_length=const.MAX_LENGTH,
                            unique=True, verbose_name="Название тэга")
    color = models.CharField(max_length=const.MAX_LENGTH, unique=True,
                             validators=[validate_color], verbose_name="Цвет")
    slug = models.SlugField(max_length=const.MAX_LENGTH, unique=True,
                            verbose_name="Слэг")

    def __str__(self) -> str:
        return self.slug

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Ingredients(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(max_length=const.MAX_LENGTH,
                            verbose_name="Название ингредиента")
    measurement_unit = models.CharField(max_length=const.MAX_LENGTH,
                                        verbose_name="Единица измерения")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recepies(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_recepies",
        verbose_name="Автор рецепта"
    )
    name = models.CharField(max_length=100, verbose_name="Название рецепта")
    image = models.ImageField(null=False, blank=False,
                              verbose_name="Изображение")
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecepIngredients'
    )
    tags = models.ManyToManyField(
        Tags,
        through='TagsRecipe'
    )
    cooking_time = models.SmallIntegerField(
        validators=[MinValueValidator(1, message='Минимальное значение = 1')],
        verbose_name="Время готовки")
    text = models.CharField(max_length=const.BIG_MAX_LENGTH,
                            verbose_name="Описание")
    favorite = models.ManyToManyField(
        UserModel,
        through="FavoriteList"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecepIngredients(models.Model):
    """Промежуточная модель рецепт-ингредиент."""
    recep = models.ForeignKey(
        Recepies,
        on_delete=models.CASCADE,
        related_name="recep_ingred",
        verbose_name="Рецепт"
    )
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент"
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1, message='Минимальное значение = 1')],
        verbose_name="Количество")

    class Meta:
        verbose_name = 'Ингредиент-рецепт'
        verbose_name_plural = 'Ингредиенты-рецепты'


class TagsRecipe(models.Model):
    """Промежуточная модель тег-рецепт."""
    recep = models.ForeignKey(
        Recepies,
        on_delete=models.CASCADE,
        related_name="raceptags",
        verbose_name="Рецепт"
    )
    tags = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        verbose_name="Тэг"
    )

    class Meta:
        verbose_name = 'Тэг-рецепт'
        verbose_name_plural = 'Тэги-рецепты'


class FavoriteList(models.Model):
    """Модель избранного."""
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_favorite",
        verbose_name="Пользователь"
    )
    recepie = models.ForeignKey(
        Recepies,
        on_delete=models.CASCADE,
        related_name="favorite_user",
        verbose_name="Рецепт"
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное_список'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recepie'], name='unique_favorite'
            )
        ]


class SubscribeList(models.Model):
    """Модель подписки."""
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_sublist",
        verbose_name="Пользователь"
    )
    subscribe = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_that_subscribe",
        verbose_name="Подписка"
    )

    class Meta:
        verbose_name = 'Список подписок'
        verbose_name_plural = 'Списки подписок'


class ShoppingList(models.Model):
    """Модель списка покупок."""
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_shopping_list",
        verbose_name="Пользователь"
    )
    recepie = models.ForeignKey(
        Recepies,
        on_delete=models.CASCADE,
        related_name="shopping_list_user",
        verbose_name="Рецепт"
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
