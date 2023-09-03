from rest_framework import permissions
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from djoser.views import UserViewSet
from .models import Client, Account
from .serializers import ClientSerializer, AccountSerializer


class ClientViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.UpdateModelMixin,mixins. DestroyModelMixin, 
                            viewsets.GenericViewSet):
    """Вьюсет для работе с моделью Client."""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('client',)
    permission_classes = (permissions.IsAuthenticated,)

class AccountViewSet(UserViewSet):
    """
    Создание/получение пользователей
    и
    создание/получение/удаления подписок.
    """

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (permissions.IsAuthenticated,)
   
    http_method_names = ['get', 'post', 'delete', 'head']
