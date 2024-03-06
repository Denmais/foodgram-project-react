from django.db import models
from users.models import UserModel
from api.validators import validate_color


class Tags(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=100, unique=True,
                             validators=[validate_color])
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self) -> str:
        return f"{self.slug}"

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Ingredients(models.Model):
    name = models.CharField(max_length=100)
    measurement_unit = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recepies(models.Model):
    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_recepies"
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(null=False, blank=False)
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecepIngredients',
    )
    tags = models.ManyToManyField(
        Tags,
        through='TagsRecipe'
    )
    cooking_time = models.SmallIntegerField()
    text = models.CharField(max_length=400)
    favorite = models.ManyToManyField(
        UserModel,
        through="FavoriteList"
    )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecepIngredients(models.Model):
    recep = models.ForeignKey(
        Recepies,
        on_delete=models.CASCADE,
        related_name="recep_ingred"
    )
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField()


class TagsRecipe(models.Model):
    recep = models.ForeignKey(
        Recepies,
        on_delete=models.CASCADE,
        related_name="raceptags"
    )
    tags = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE
    )


class FavoriteList(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_favorite"
    )
    recepie = models.ForeignKey(
        Recepies,
        on_delete=models.CASCADE,
        related_name="favorite_user"
    )


class SubscribeList(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_sublist"
    )
    subscribe = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_that_subscribe"
    )


class ShoppingList(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_shopping_list"
    )
    recepie = models.ForeignKey(
        Recepies,
        on_delete=models.CASCADE,
        related_name="shopping_list_user"
    )
