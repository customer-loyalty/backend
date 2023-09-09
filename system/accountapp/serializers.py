from rest_framework import serializers
from django.db.models import F
from djoser.serializers import UserCreateSerializer

from .models import Client, Сard, Account, TypeCard, Сard, PurchaseAmount

class СardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'cardType','cardId', 'bonusBalance')
        model = Сard

class PurchaseAmountSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = PurchaseAmount
        fields = ('id','total_amount',) #сделать 2 сериалайзера 'card' - #c) 

    def update(self, instance, validated_data):
        print(validated_data)
        card_id = validated_data['card']
        print(card_id)
        amount= validated_data['total_amount']
        print(amount)
        PurchaseAmount.objects.filter(card=card_id).update(total_amount=F('total_amount') + amount)
        return instance

      
class ClientSerializer(serializers.ModelSerializer):
    """Класс - сериализатор модели Client для get запроса"""
    reg = serializers.DateTimeField(format="%Y-%m-%d")
    purchase_amount= PurchaseAmountSerializer()
    card = СardSerializer()
    class Meta:
        model = Client
        fields = ('id','name', 'surname', 'birthday', 'gender',
                  'reg', 'phone_number', 'client', 'card', 'purchase_amount',)
    
class ClientPostSerializer(ClientSerializer):
                           

    def create(self, validated_data):
        request = self.context.get('request', None)
        card = validated_data.pop('card')
        purchase = validated_data.pop('purchase_amount')
        #purchase.pop('card')
        print(card, purchase, 1)
        card = Сard.objects.create (**card)
        card_id= Сard.objects.latest('id')
        
        print(card_id, 2)
        purchase = PurchaseAmount.objects.create (**purchase, card =card_id)
        purchase_amount_id= PurchaseAmount.objects.latest('id')
        print(purchase, 3)
        client = Client.objects.create(**validated_data, card =card_id, purchase_amount=purchase_amount_id)
        print(client, 4)
        return client
       
class ClientUpdateSerializer(serializers.ModelSerializer):
    """Класс - сериализатор модели Client для update запроса"""
    reg = serializers.DateTimeField(format="%Y-%m-%d")
   
    class Meta:
        model = Client
        fields = ('id','name', 'surname', 'birthday', 'gender',
                  'reg', 'phone_number', 'client')
        


    '''def update(self, instance, validated_data):
        card_data = validated_data.pop('card', {})
        bonus_card =  card_data['bonusBalance']
        bonus_cardId=card_data['cardId']
        print(bonus_cardId, 2)
        old = Сard.objects.get(cardId = bonus_cardId).bonusBalance
        print(old)
        bonus = old + bonus_card
        card_data['bonusBalance'] = bonus
        card_serializer = СardSerializer(instance.card, data=card_data)
        card_serializer.is_valid(raise_exception=True)
        card_serializer.save()
        return super().update(instance, validated_data)'''
    

class AccountSerializer(UserCreateSerializer):
    """Кастомизация пользователя из Djoser."""
    
   
    class Meta:
        model = Account
        fields = ('username', 'email',  
                  'phone_number',  'password',
                  'first_name', 'last_name')  
        

class TypeCardtSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = TypeCard
        fields = ('name', 'purchase_amount',  
                  'rate_field',  'account',) 



        
       
                     
