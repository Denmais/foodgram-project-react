from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import (UserCreateSerializer, UsersSerializer,
                               UserTokenSerializer, ResetPasswordSeriazlizer)
from api.serializers import SubscribeSerializer, SubscribeLimitSerializer
from users.models import UserModel
from rest_framework.settings import api_settings
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from api.models import SubscribeList, Recepies


class RegisterUser(APIView):
    permission_classes = (permissions.AllowAny,)
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        print(self.pagination_class)
        users = UserModel.objects.all()
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = UsersSerializer(page, many=True,
                                         context={"request": request})
            return self.get_paginated_response(serializer.data)

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
        print(limit)
        if limit is not None:
            self.paginator.page_size = limit
        return self.paginator.paginate_queryset(queryset, self.request,
                                                view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class DetailUser(APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, request, pk):
        try:
            user = UserModel.objects.get(pk=pk)
        except UserModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UsersSerializer(user, context={"request": request})
        return Response(serializer.data)


class MeUser(APIView):

    def get(self, request):
        print(request.user)
        user = UserModel.objects.get(username=request.user.username)
        serializer = UsersSerializer(user, context={"request": request})
        return Response(serializer.data)


class GetTokenView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        user = get_object_or_404(UserModel, email=email)
        try:
            token = Token.objects.get(user=user)
            token.delete()
            token = Token.objects.create(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        return Response({'auth_token': str(token)},
                        status=status.HTTP_200_OK)


class ResetPasswordView(APIView):

    def post(self, request):
        user = request.user
        serializer = ResetPasswordSeriazlizer(data=request.data,
                                              context={'request': request})
        serializer.is_valid(raise_exception=True)
        user.password = serializer.validated_data['new_password']
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogoutView(APIView):

    def post(self, request):
        Token.objects.get(key=request.auth).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeView(APIView):

    def post(self, request, pk):
        user = request.user
        try:
            author = UserModel.objects.get(pk=pk)
        except UserModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if ((SubscribeList.objects.filter(user=user, subscribe=author)
             .exists()) or (author == user)):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        recipes_limit = self.request.query_params.get('recipes_limit')
        SubscribeList.objects.create(user=user, subscribe=author)
        if recipes_limit is not None:
            author.limit_recepies = Recepies.objects.all()[:int(recipes_limit)]
            serializer = SubscribeLimitSerializer(author,
                                                  context={"request": request})
        else:
            serializer = SubscribeSerializer(author,
                                             context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = request.user
        try:
            author = UserModel.objects.get(pk=pk)
        except UserModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not SubscribeList.objects.filter(user=user,
                                            subscribe=author).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        SubscribeList.objects.get(user=user, subscribe=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeListView(APIView):

    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get(self, request):
        user = request.user
        print(user)
        subscribes = UserModel.objects.filter(
            user_that_subscribe__user=user.pk)
        print(UserModel.objects.filter(user_that_subscribe__user=user.pk))
        recipes_limit = self.request.query_params.get('recipes_limit')
        if recipes_limit is not None:
            for i in subscribes:
                i.limit_recepies = Recepies.objects.all()[:int(recipes_limit)]
        page = self.paginate_queryset(subscribes)
        if page is not None:
            if recipes_limit is not None:
                serializer = SubscribeLimitSerializer(page, many=True,
                                                      context={"request":
                                                               request})
            else:
                serializer = SubscribeSerializer(page, many=True,
                                                 context={"request": request})
            return self.get_paginated_response(serializer.data)

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
        return self.paginator.paginate_queryset(queryset,
                                                self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
