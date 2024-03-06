from rest_framework import serializers
from .models import (Tags, Ingredients, Recepies,
                     RecepIngredients, TagsRecipe, FavoriteList, ShoppingList)
from users.models import UserModel
from django.shortcuts import get_object_or_404
from users.serializers import UsersSerializer
import base64  # Модуль с функциями кодирования и декодирования base64
from django.db.models import Count
from django.core.files.base import ContentFile


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = "__all__"


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = "__all__"


class IngredientsInRecepieSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source="ingredients.name")
    measurement_unit = serializers.CharField(
        source="ingredients.measurement_unit")

    class Meta:
        model = RecepIngredients
        fields = ("id", "name", "amount", "measurement_unit")


class IngredientsInRecepieCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(read_only=True, source="ingredients.name")
    measurement_unit = serializers.CharField(
        read_only=True, source="ingredients.measurement_unit")

    class Meta:
        model = RecepIngredients
        fields = ("id", "amount", "name", "measurement_unit")


class RecepiesSerializer(serializers.ModelSerializer):
    ingredients = IngredientsInRecepieSerializer(many=True,
                                                 source="recep_ingred")
    tags = TagsSerializer(many=True)
    author = UsersSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return FavoriteList.objects.filter(
                user=self.context['request'].user, recepie=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingList.objects.filter(
                user=self.context['request'].user, recepie=obj).exists()
        return False

    class Meta:
        model = Recepies
        exclude = ("favorite",)


class TagsCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Tags
        fields = ("id",)


class RecepiesCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientsInRecepieCreateSerializer(many=True,
                                                       source="recep_ingred")
    tags = serializers.ListSerializer(child=serializers.IntegerField())
    author = UsersSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    def create(self, validated_data):
        ingredients = validated_data.pop("recep_ingred")
        tags = validated_data.pop('tags')
        print(ingredients)

        recepie = Recepies.objects.create(**validated_data)

        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient = get_object_or_404(Ingredients, pk=ingredient['id'])

            RecepIngredients.objects.create(
                amount=amount,
                ingredients=ingredient,
                recep=recepie
            )
        for tag in tags:
            tag = get_object_or_404(Tags, pk=tag)
            TagsRecipe.objects.create(
                recep=recepie,
                tags=tag
            )
        return recepie

    def update(self, instance, validated_data):
        print(instance.author)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.ingredients.clear()

        ingredients_data = validated_data.pop('recep_ingred')
        for ingredients in ingredients_data:
            RecepIngredients.objects.create(recep_id=instance.id,
                                            ingredients_id=ingredients['id'],
                                            amount=ingredients['amount'])
        ls = []
        tag_data = validated_data.pop('tags')
        for tags in tag_data:
            tag = get_object_or_404(Tags, pk=tags)
            ls.append(tag)
        instance.tags.set(ls)

        instance.save()
        return instance

    def validate_ingredients(self, value):
        if len(value) == 0:
            raise serializers.ValidationError('Поле ингредиентов пусто!')
        dict_of_ingr = {}
        for ingredient in value:
            print(ingredient['amount'])
            if not Ingredients.objects.filter(pk=ingredient['id']).exists():
                raise serializers.ValidationError(
                    f"Ингредиент с id {ingredient['id']} не существует!")
            if ingredient['id'] in dict_of_ingr:
                raise serializers.ValidationError("Повторяющийся ингредиент!")
            dict_of_ingr[ingredient['id']] = 1
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError("Отрицательное количество!")
        return value

    def validate_tags(self, value):
        if len(value) == 0:
            raise serializers.ValidationError('Поле тегов пусто!')
        dict_of_tags = {}
        for tag in value:
            print(tag)
            if not Tags.objects.filter(pk=tag).exists():
                raise serializers.ValidationError(
                    f"Тег с id {tag} не существует!")
            if tag in dict_of_tags:
                raise serializers.ValidationError("Повторяющийся тег!")
            dict_of_tags[tag] = 1
        return value

    def validate_cooking_time(self, value):
        if value < 1:
            raise serializers.ValidationError('Ошибка времени приготовления!')
        return value

    def validate(self, data):
        print('recep_ingred' in data)
        if 'recep_ingred' not in data:
            raise serializers.ValidationError(
                "Поле ингредиентов - обязательное!")
        if 'tags' not in data:
            raise serializers.ValidationError("Поле тегов - обязательное!")
        if 'image' not in data:
            raise serializers.ValidationError(
                "Поле изображения - обязательное!")
        return data

    def to_representation(self, instance):
        serializers = RecepiesSerializer(instance, context=self.context)
        return serializers.data

    class Meta:
        model = Recepies
        fields = ("id", "author", "ingredients",
                  "cooking_time", "text", "name", "tags", "image")
        read_only_fields = ('author',)


class FavoriteListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recepies
        fields = ("id", "cooking_time", "name", "image")


class SubscribeSerializer(UsersSerializer):

    recipes = FavoriteListSerializer(many=True, source="user_recepies")
    recipes_count = serializers.SerializerMethodField()

    def get_recipes_count(self, obj):
        return UserModel.objects.filter(pk=obj.pk).aggregate(
            Count('user_recepies'))['user_recepies__count']

    class Meta:
        model = UserModel
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count"
        )


class SubscribeLimitSerializer(UsersSerializer):

    recipes = FavoriteListSerializer(many=True, source="limit_recepies")
    recipes_count = serializers.SerializerMethodField()

    def get_recipes_count(self, obj):
        return UserModel.objects.filter(pk=obj.pk).aggregate(
            Count('user_recepies'))['user_recepies__count']

    class Meta:
        model = UserModel
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count"
        )
