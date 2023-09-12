from rest_framework import serializers
from django.db.models import F
from djoser.serializers import UserCreateSerializer
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from .models import Client, Сard, Account, TypeCard, Сard, PurchaseAmount
from system.settings import EMAIL_HOST_USER

Create_client_messenge = f'Вы успешно зарегистрированы' 

class СardSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'cardType','cardId', 'bonusBalance')
        model = Сard

class СardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "cardType", "cardId", "bonusBalance")
        model = Сard

   



class PurchaseAmountSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = PurchaseAmount
        fields = ('id','total_amount') #сделать 2 сериалайзера 'card' - #c)


    @staticmethod
    def update_card_type(card_id):
        total_amount = PurchaseAmount.objects.get(card=card_id).total_amount
        print(total_amount, 1)
        card_types = TypeCard.objects.all()
        print(card_types, 2)
        c =  card_types[0]
        print(c.purchase_amount, 3)
        for card_type in card_types:
            if c.purchase_amount <= card_type.purchase_amount <= total_amount:
                c = card_type
        print(c, card_id)
        card_id.cardType = c
        print(c, 6)
        card_id.save()
        return c



    def update(self, instance, validated_data):
        print(validated_data)
        card_id = validated_data['card']
        print(card_id)
        amount= validated_data['total_amount']
        print(amount)
        PurchaseAmount.objects.filter(card=card_id).update(total_amount=F('total_amount') + amount)
        PurchaseAmountSerializer.update_card_type(card_id)
        # send_mail('Тема', 'Покупка', settings.EMAIL_HOST_USER, to=['A60874022@yandex.ru'], fail_silently=False,)
        return instance
    
    
      
class ClientSerializer(serializers.ModelSerializer):
    """Класс - сериализатор модели Client для get запроса"""
    reg = serializers.DateTimeField(format="%Y-%m-%d")
    purchase_amount= PurchaseAmountSerializer()
    card = СardSerializer()
    class Meta:
        model = Client
        fields = ('id','name', 'surname', 'birthday', 'gender', 'mail',
                  'reg', 'phone_number', 'client', 'card', 'purchase_amount',)
    


class ClientPostSerializer(ClientSerializer):
                           

    def create(self, validated_data):
        request = self.context.get('request', None)
        card = validated_data.pop('card')
        purchase = validated_data.pop('purchase_amount')
        Сard.objects.create (**card)
        card_id= Сard.objects.latest('id')
        purchase = PurchaseAmount.objects.create (**purchase, card =card_id)
        purchase_amount_id= PurchaseAmount.objects.latest('id')
        client = Client.objects.create(**validated_data, card =card_id, purchase_amount=purchase_amount_id)
        client_name = validated_data['name']
        bonusBalance =  card['bonusBalance']
        client_email = validated_data['mail']
        create_client_messenge = (f'{client_name}, здравствуйте. '
                                 f'Спасибо за регистрацию. Вам начислено {bonusBalance}. Текущий баланс {bonusBalance}.')
        send_mail('rkbt', create_client_messenge, settings.EMAIL_HOST_USER, [client_email])
        return client




class ClientUpdateSerializer(serializers.ModelSerializer):
    """Класс - сериализатор модели Client для update запроса"""
    reg = serializers.DateTimeField(format="%Y-%m-%d")
   
    class Meta:
        model = Client
        fields = ('id','name', 'surname', 'birthday', 'gender', 'mail',
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



        
       
                     
