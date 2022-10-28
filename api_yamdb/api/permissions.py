from rest_framework import permissions


class Moderator(permissions.BasePermission):
    """Класс модератор"""

    def has_object_permission(self, request, view, obj):
        return request.method == 'DELETE' and request.user.is_moderator


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Класс Аутентифицированный пользователь.

     Разрешает безопасные методы всем,
     изменение и удаление владельцам, удаление модераторам"""

    def has_permission(self, request, view):
        return request.method == 'GET' or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if (
            request.method in permissions.SAFE_METHODS
            or request.method == 'DELETE' and request.user.is_moderator
        ):
            return True
        return obj.author == request.user


class AdminOnly(permissions.BasePermission):
    """Допуск для admin или superuser"""

    def has_permission(self, request, view,):
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )


class AdminOrReadOnly(permissions.BasePermission):
    """Разрешает safe операции при авторизации.

     Полный доступ admin или superuser.
     """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )
