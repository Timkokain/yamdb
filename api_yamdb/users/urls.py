from django.urls import include, path
from rest_framework import routers

from users.views import (RegistrationAPIView,
                         TokenRegistrationAPIView, UsersViewSet)

app_name = 'users'

router = routers.SimpleRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', RegistrationAPIView.as_view(), name='signup'),
    path('v1/auth/token/', TokenRegistrationAPIView.as_view(), name='token'),

]
