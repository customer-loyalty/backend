from rest_framework import serializers
from django.db.models import F
from djoser.serializers import UserCreateSerializer
from django.conf import settings
from django.core.mail import send_mail

from .models import Client, Card, Account, TypeCard, PurchaseAmount


class CardBonusSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с картами клиента"""

    class Meta:
        model = Card
        fields = ("id", "cardType", "cardId", "bonusBalance")


class CardBonusPostSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с картами клиента"""

    class Meta:
        model = Card
        fields = ("id", "cardType", "cardId",)
    

class CardBonusUpdateSerializer(CardBonusSerializer):
    """Сериалайзер для работы с картами клиента"""

    def update(self, instance, validated_data):
        print(validated_data)
        card_id = validated_data['cardId']
        bonusBalance = validated_data['bonusBalance']
        Card.objects.filter(cardId=card_id).update(bonusBalance=F('bonusBalance')
                                                   + bonusBalance)
        return instance


class PurchaseAmountPostSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с покупками при создании клиента"""
    class Meta:
        model = PurchaseAmount
        fields = ('id', 'total_amount',)


class PurchaseAmountSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы c покупками клиента"""
    class Meta:
        model = PurchaseAmount
        fields = ('id', 'total_amount', 'card',)

    @staticmethod
    def update_card_type(card_id):
        """функция выбора карты при изменении суммы покупок"""
        total_amount = PurchaseAmount.objects.get(card=card_id).total_amount
        card_types = TypeCard.objects.all()
        c = card_types[0]
        for card_type in card_types:
            if c.purchase_amount <= card_type.purchase_amount <= total_amount:
                c = card_type
        card_id.cardType = c
        card_id.save()
        return c

    def update(self, instance, validated_data):
        card_id = validated_data['card']
        amount = validated_data['total_amount']
        PurchaseAmount.objects.filter(card=card_id).update(total_amount=F('total_amount')
                                                           + amount)
        PurchaseAmountSerializer.update_card_type(card_id)
        return instance


class ClientSerializer(serializers.ModelSerializer):
    """Класс - сериализатор модели Client для get запроса"""
    reg = serializers.DateTimeField(format="%Y-%m-%d")
    purchase_amount = PurchaseAmountPostSerializer()
    card = CardBonusSerializer()

    class Meta:
        model = Client
        fields = ('id', 'name', 'surname', 'birthday', 'gender', 'mail',
                  'reg', 'phone_number', 'client', 'card', 'purchase_amount',)


class ClientPostSerializer(ClientSerializer):
    """Класс - сериализатор модели Client для post запроса"""
    card = CardBonusPostSerializer()

    def create(self, validated_data):
        request = self.context.get('request', None)
        card = validated_data.pop('card')
        print(card['cardType'], 456)
        bonus = card['cardType'].initial_bonuses
        print(bonus, 124)
        purchase = validated_data.pop('purchase_amount')
        Card.objects.create(**card, bonusBalance=bonus)
        card_id = Card.objects.latest('id')
        purchase = PurchaseAmount.objects.create(**purchase, card=card_id)
        purchase_amount_id = PurchaseAmount.objects.latest('id')
        client = Client.objects.create(**validated_data,
                                       card=card_id,
                                       purchase_amount=purchase_amount_id)
        client_name = validated_data['name']
        print(client_name, 125)
        client_email = validated_data['mail']
        create_client_messenge = (f'{client_name}, Здравствуйте. '
                                  f'Спасибо за регистрацию. '
                                  f'Вам начислено {bonus}. '
                                  f'Текущий баланс {bonus}.')
        send_mail('Тема', create_client_messenge,
                  settings.EMAIL_HOST_USER, [client_email])
        return client


class ClientUpdateSerializer(serializers.ModelSerializer):
    """Класс - сериализатор модели Client для update запроса"""
    reg = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Client
        fields = ('id', 'name', 'surname', 'birthday', 'gender', 'mail',
                  'reg', 'phone_number', 'client',)


class AccountSerializer(UserCreateSerializer):
    """Кастомизация пользователя из Djoser."""

    class Meta:
        model = Account
        fields = ('username', 'url', 'activity',
                  'аddress', 'email', 'password',
                  'first_name', 'last_name')


class TypeCardtSerializer(serializers.ModelSerializer):
    """Cериалайзер для работы с типами карт"""

    class Meta:
        model = TypeCard
        fields = ('id', 'name', 'purchase_amount', 'initial_bonuses',
                  'rate_field',  'account',)
