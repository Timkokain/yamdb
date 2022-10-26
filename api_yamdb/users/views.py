import logging

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import AdminOnly
from users.exceptions import TokenGenError
from users.serializers import (GetTokenSerializer, RegistrationSerializer,
                               RestrictUsersSerializer, UsersSerializer)
from users.utils import send_confirmation_email

User = get_user_model()

logger = logging.getLogger(__name__)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = "username"
    permission_classes = [AdminOnly, ]
    serializer_class = UsersSerializer
    pagination_class = PageNumberPagination
    search_fields = ('username',)
    filter_backends = (filters.SearchFilter,)

    def perform_create(self, serializer):
        serializer.save(is_active=True)

    @action(
        detail=False,
        methods=['get', 'patch', ],
        permission_classes=[IsAuthenticated, ],
        url_path='me'
    )
    def me_viewset(self, request):
        user = request.user
        serializer = (
            UsersSerializer if user.is_staff else RestrictUsersSerializer
        )
        if request.method == 'GET':
            return Response(
                serializer(user).data,
                status=status.HTTP_200_OK
            )
        if request.method == 'PATCH':
            serializer = serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        serializer.save(is_active=True)
        send_confirmation_email(serializer.instance)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = 200
        return response


class TokenRegistrationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data['username']
        )
        if not serializer.validated_data['password'] == user.password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            token = {"token": user.token}
        except TokenGenError as error:
            logger.exception(error)
        else:
            user.is_active = True
            user.save(update_fields=["is_active"])
            return Response(token, status=status.HTTP_200_OK)
