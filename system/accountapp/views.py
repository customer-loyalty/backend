
from .models import Client
# Create your views here.
from .serializers import ClientSerializer
from rest_framework import viewsets

class ClientViewSet(viewsets.ModelViewSet):
    """Вьюсет для работе с моделью Recipe."""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
   
    