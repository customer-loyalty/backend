from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins

from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.UpdateModelMixin,mixins. DestroyModelMixin, 
                            viewsets.GenericViewSet):
    """Вьюсет для работе с моделью Client."""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('client',)
    permission_classes = (permissions.IsAuthenticated,)
