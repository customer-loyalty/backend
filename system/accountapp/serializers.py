from rest_framework import serializers
from django.http import HttpResponse
from phonenumber_field.serializerfields import PhoneNumberField
from djoser.serializers import UserCreateSerializer
from rest_framework import status
from .models import Client, Сard, Account
from rest_framework.response import Response
class СardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('cardType','cardId', 'bonusBalance')
        model = Сard


class ClientSerializer(serializers.ModelSerializer):
    """Класс - сериализатор модели """
    reg = serializers.DateTimeField(format="%Y-%m-%d")
    card = СardSerializer()
    class Meta:
        model = Client
        fields = ('id','name', 'surname', 'middleName', 'birthday', 'gender',
                  'reg', 'telegram', 'phone_number', 'client', 'card')
    

    def create(self, validated_data):
        request = self.context.get('request', None)
        card = validated_data.pop('card')
        print(card, 1)
        card = Сard.objects.create (**card)
        print(card, 2)
        card_id= Сard.objects.latest('id')
        print(card_id, 3)
        client = Client.objects.create(**validated_data, card =card_id)
        print(4)
        return client
       
    
    def update(self, instance, validated_data):
        card_data = validated_data.pop('card', {})
        
        bonus_card =  card_data['bonusBalance']
        bonus_cardId=card_data['cardId']
        print(bonus_cardId, 2)
        old = Сard.objects.get(cardId = bonus_cardId)
        bonus = old.bonusBalance + bonus_card
        print(bonus_card, 1)
        print(old.bonusBalance, bonus_card, bonus, 3)
        card_data['bonusBalance'] = bonus
        card_serializer = СardSerializer(instance.card, data=card_data)
        card_serializer.is_valid(raise_exception=True)
        card_serializer.save()
        return super().update(instance, validated_data)

class AccountSerializer(UserCreateSerializer):
    """Кастомизация пользователя из Djoser."""
    
   

    class Meta:
        model = Account
        fields = ('username', 'email',  
                  'phone_number',  'password',
                  'first_name', 'last_name')  
        
   




