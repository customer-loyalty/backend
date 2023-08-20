from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    """Класс - сериализатор модели """
    client = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Client
        fields = '__all__'
