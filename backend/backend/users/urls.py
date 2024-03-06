from django.urls import path
from users.views import (RegisterUser, DetailUser, MeUser, GetTokenView,
                         ResetPasswordView, LogoutView,
                         SubscribeView, SubscribeListView)

urlpatterns = [
    path('<int:pk>/', DetailUser.as_view()),
    path('subscriptions/', SubscribeListView.as_view()),
    path('<int:pk>/subscribe/', SubscribeView.as_view()),
    path('token/login/', GetTokenView.as_view()),
    path('token/logout/', LogoutView.as_view()),
    path('set_password/', ResetPasswordView.as_view()),
    path('me/', MeUser.as_view()),
    path('', RegisterUser.as_view())
]
