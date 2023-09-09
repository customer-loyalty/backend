from rest_framework import permissions
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from djoser.views import UserViewSet
from .models import Client, Account, TypeCard, PurchaseAmount
from .serializers import ClientSerializer, AccountSerializer, TypeCardtSerializer, PurchaseAmountSerializer


class ClientViewSet(viewsets.ModelViewSet):
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


class TypeCardViewSet(viewsets.ModelViewSet):
    """Вьюсет для работе с моделью Client."""
    queryset = TypeCard.objects.all()
    serializer_class = TypeCardtSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PurchaseAmountViewSet(viewsets.ModelViewSet):
    """Вьюсет для работе с моделью Client."""
    queryset = PurchaseAmount.objects.all()
    serializer_class = PurchaseAmountSerializer
    permission_classes = (permissions.IsAuthenticated,)