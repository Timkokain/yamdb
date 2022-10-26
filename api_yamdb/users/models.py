from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from .managers import CustomUserManager
from .validators import me_validator


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя

    Поля email и username обязательны.
    """

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE_CHOICES = (
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
        (USER, USER),
    )

    username = models.CharField(
        verbose_name='user',
        max_length=150,
        db_index=True,
        unique=True,
        validators=[me_validator]
    )
    email = models.EmailField(
        verbose_name='email',
        max_length=254,
        db_index=True,
        unique=True
    )
    password = models.CharField(max_length=150,)
    first_name = models.CharField(max_length=150, blank=True, default='',)
    last_name = models.CharField(max_length=150, blank=True, default='',)
    bio = models.TextField(blank=True, default='',)
    role = models.CharField(
        choices=ROLE_CHOICES, max_length=150, default=USER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

    @property
    def is_superuser(self):
        return self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def conformation_token(self):
        return self._conformation_token()

    def _conformation_token(self):
        self.password = CustomUser.objects.make_random_password(length=10)
        self.save(update_fields=['password'])
        return self.password

    @property
    def token(self):
        """Для создания токена можно использовать user.token"""
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Создает JWT Token
        """

        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)
