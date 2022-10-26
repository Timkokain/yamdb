from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер моделей пользователей"""

    def create_user(self, username, email, **extra_fields):
        return self._create_user(username, email, **extra_fields)

    def _create_user(self, username, email, **extra_fields):
        """Создание и сохранение user с присвоенным usernsme, email"""
        if not username:
            raise ValueError('Необходимо указать имя пользователя')
        if not email:
            raise ValueError('Необходимо указать email')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = self.make_random_password(length=10)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, **extra_fields):
        """Создание и сохранение superuser с присвоенным usernsme, email."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', self.model.ADMIN)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        return self._create_user(username, email, **extra_fields)
