from django.urls import path, include
from rest_framework import routers
from api.views import (TagViewSet, IngredientViewSet, RecepieList,
                       RecepieDetail, FavoriteView, ShoppingListView,
                       ShopListCreateView)


router_v1 = routers.DefaultRouter()
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
urlpatterns = [
    path('', include(router_v1.urls)),
    path('recipes/', RecepieList.as_view()),
    path('recipes/<int:pk>/', RecepieDetail.as_view()),
    path('recipes/download_shopping_cart/', ShopListCreateView.as_view()),
    path('recipes/<int:pk>/shopping_cart/', ShoppingListView.as_view()),
    path('recipes/<int:pk>/favorite/', FavoriteView.as_view())
]
