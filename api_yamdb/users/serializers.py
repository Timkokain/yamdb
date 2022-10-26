from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор текущей модели User.

    Все поля доступны для любых операций
    """

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class RestrictUsersSerializer(UsersSerializer):
    """Сериализатор текущей модели User.

    Поле role только для чтения
    """

    class Meta(UsersSerializer.Meta):
        read_only_fields = ['role', ]


class RegistrationSerializer(serializers.ModelSerializer):
    """Создание user. Оправка письма с паролем на получение токена."""

    class Meta:
        model = User
        fields = ['email', 'username']

    def create(self, validated_data):
        return User.objects._create_user(**validated_data)


class GetTokenSerializer(serializers.Serializer):
    """Получение токена в ответ на confirmation_code."""

    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(
        source='password', required=True, max_length=150)

    class Meta:
        fields = ['username', 'confirmation_code']
