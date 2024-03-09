from rest_framework import serializers
from users.models import UserModel
from users.validators import validate_forbidden_username
from api.models import SubscribeList
from rest_framework.validators import UniqueValidator


class UsersSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        author = obj
        if user.is_authenticated:
            return SubscribeList.objects.filter(user=user,
                                                subscribe=author).exists()
        return False

    class Meta:
        model = UserModel
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed"
        )


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'id')
        model = UserModel


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""
    username = serializers.CharField(max_length=100,
                                     required=True,
                                     validators=[validate_forbidden_username,
                                                 UniqueValidator(
                                                     queryset=UserModel.
                                                     objects.all())])

    def to_representation(self, instance):
        serializers = UserGetSerializer(instance)
        return serializers.data

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password')
        model = UserModel


class UserTokenSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=154, required=True)
    password = serializers.CharField(max_length=154, required=True)

    def validate(self, data):
        """Проверка при введении правильного пароля или почты."""
        if (UserModel.objects.filter(password=data['password']).exists()
                and not UserModel.objects
                .filter(email=data['email']).exists()):
            raise serializers.ValidationError(
                'Ошибка, проверьте правильность почты!')
        elif (not UserModel.objects.filter(password=data['password']).exists()
              and UserModel.objects.filter(email=data['email']).exists()):
            raise serializers.ValidationError(
                'Ошибка, проверьте правильность пароль!')
        elif not UserModel.objects.filter(password=data['password'],
                                          email=data['email']).exists():
            raise serializers.ValidationError("Ошибка авторизации!")
        return data


class ResetPasswordSeriazlizer(serializers.Serializer):
    new_password = serializers.CharField(max_length=100)
    current_password = serializers.CharField(max_length=100)

    def validate(self, data):
        user = self.context['request'].user
        if user.password != data['current_password']:
            raise serializers.ValidationError(
                "Проверьте правильность пароля!"
            )
        return data
