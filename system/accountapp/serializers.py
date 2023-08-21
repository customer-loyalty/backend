from rest_framework import serializers

from .models import Client, Сard

class СardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('balance','cardId')
        model = Сard


class ClientSerializer(serializers.ModelSerializer):
    """Класс - сериализатор модели """
    client = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d")
    card = СardSerializer(read_only=True)
    class Meta:
        model = Client
        fields = ('id','first_name', 'last_name', 'patronymic1', 'dob', 'sex',
                  'created_at', 'telegram', 'phone_number', 'client', 'card')
                  


