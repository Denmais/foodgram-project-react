from rest_framework import viewsets, permissions, filters
from .models import Tags, Ingredients, Recepies, FavoriteList, ShoppingList
from users.models import UserModel
from .serializers import (TagsSerializer, IngredientsSerializer,
                          RecepiesSerializer, RecepiesCreateSerializer,
                          FavoriteListSerializer)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework import status
from api.permissions import OwnerOrReadOnly
from django.http import HttpResponse


class TagViewSet(viewsets.ModelViewSet):
    """Вьюсет для тэгов."""
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get']
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет для ингредиентов."""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = None


class RecepieList(APIView):
    """Представление рецептов."""
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    permission_classes = (OwnerOrReadOnly,)

    def get(self, request):
        user = request.user
        authors = dict(self.request.query_params).get("author")
        tags = dict(self.request.query_params).get("tags")
        is_is_shopping_cart = dict(self.request.query_params).get(
            "is_in_shopping_cart")
        is_favorite = dict(self.request.query_params).get("is_favorited")
        recepies = Recepies.objects.all()
        if tags is not None:
            recepies = recepies.filter(
                raceptags__tags__slug__in=tags).distinct()
        if is_is_shopping_cart is not None:
            if is_is_shopping_cart[0] == '1' and user.is_authenticated:
                recepies = recepies.filter(shopping_list_user__user=user)
            else:
                recepies = recepies.filter(author_id=0)
        if is_favorite is not None:
            if is_favorite[0] == '1' and user.is_authenticated:
                recepies = recepies.filter(favorite_user__user=user)
            else:
                recepies = recepies.filter(author_id=0)
        if authors is not None:
            recepies = recepies.filter(author__in=authors)
        page = self.paginate_queryset(recepies)
        if page is not None:
            serializer = RecepiesSerializer(page, many=True,
                                            context={'request': request})
            return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = RecepiesCreateSerializer(data=request.data,
                                              context={'request': request})
        user = request.user
        serializer.is_valid(raise_exception=True)
        serializer.save(author=UserModel.objects.get(username=user.username))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        limit = self.request.query_params.get('limit')
        if limit is not None:
            self.paginator.page_size = limit
        return self.paginator.paginate_queryset(
            queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class RecepieDetail(APIView):
    """Представление рецепта."""
    permission_classes = (OwnerOrReadOnly,)

    def get(self, request, pk):
        recepie = Recepies.objects.get(pk=pk)
        serializer = RecepiesSerializer(recepie, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            recipe = Recepies.objects.get(pk=pk)
        except Recepies.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, recipe)
        serializer = RecepiesCreateSerializer(recipe,
                                              data=request.data, partial=True,
                                              context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            recipe = Recepies.objects.get(pk=pk)
        except Recepies.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, recipe)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteView(APIView):
    """Представление избранного."""
    def post(self, request, pk):
        user = request.user
        try:
            recepie = Recepies.objects.get(pk=pk)
        except Recepies.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if FavoriteList.objects.filter(user=user, recepie=recepie).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        FavoriteList.objects.create(user=user, recepie=recepie)
        serializer = FavoriteListSerializer(recepie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = request.user
        try:
            recepie = Recepies.objects.get(pk=pk)
        except Recepies.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not FavoriteList.objects.filter(user=user,
                                           recepie=recepie).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        FavoriteList.objects.get(user=user, recepie=recepie).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingListView(APIView):
    """Представление списка покупок."""
    def post(self, request, pk):
        user = request.user
        try:
            recepie = Recepies.objects.get(pk=pk)
        except Recepies.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if ShoppingList.objects.filter(user=user, recepie=recepie).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ShoppingList.objects.create(user=user, recepie=recepie)
        serializer = FavoriteListSerializer(recepie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = request.user
        try:
            recepie = Recepies.objects.get(pk=pk)
        except Recepies.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not ShoppingList.objects.filter(user=user,
                                           recepie=recepie).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ShoppingList.objects.get(user=user, recepie=recepie).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShopListCreateView(APIView):
    """Представление создания списка покупок."""
    permission_classes = (OwnerOrReadOnly,)

    def get(self, request):
        ingr_dict = {}
        shop_list = ShoppingList.objects.filter(user=request.user)
        values = shop_list.values('recepie__ingredients__name',
                                  'recepie__ingredients__measurement_unit',
                                  'recepie__recep_ingred__amount')
        for value in values:
            if value['recepie__ingredients__name'] not in ingr_dict:
                ingr_dict[value['recepie__ingredients__name']] = [value[
                    'recepie__ingredients__measurement_unit'], 0]
            ingr_dict[value['recepie__ingredients__name']][1] += value[
                'recepie__recep_ingred__amount']

        resp = "     Продукты           Количество\n"
        for i in ingr_dict:
            resp += (
                f"**** {i}({ingr_dict[i][0]}) ----------- {ingr_dict[i][1]}\n")

        return HttpResponse(resp, content_type="text/plain")
