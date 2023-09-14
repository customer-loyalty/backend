from rest_framework import serializers
from django.db.models import F
from djoser.serializers import UserCreateSerializer
from django.conf import settings
from django.core.mail import send_mail

from .models import Client, Сard, Account, TypeCard, PurchaseAmount


class СardSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с картами клиента"""

    class Meta:
        fields = ("id", "cardType", "cardId", "bonusBalance")
        model = Сard


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
        # send_mail('Тема', 'Покупка', settings.EMAIL_HOST_USER,
        # to=['A60874022@yandex.ru'], fail_silently=False,)
        return instance


class ClientSerializer(serializers.ModelSerializer):
    """Класс - сериализатор модели Client для get запроса"""
    reg = serializers.DateTimeField(format="%Y-%m-%d")
    purchase_amount = PurchaseAmountPostSerializer()
    card = СardSerializer()

    class Meta:
        model = Client
        fields = ('id', 'name', 'surname', 'birthday', 'gender', 'mail',
                  'reg', 'phone_number', 'client', 'card', 'purchase_amount',)


class ClientPostSerializer(ClientSerializer):
    """Класс - сериализатор модели Client для post запроса"""

    def create(self, validated_data):
        request = self.context.get('request', None)
        card = validated_data.pop('card')
        purchase = validated_data.pop('purchase_amount')
        Сard.objects.create(**card)
        card_id = Сard.objects.latest('id')
        purchase = PurchaseAmount.objects.create(**purchase, card=card_id)
        purchase_amount_id = PurchaseAmount.objects.latest('id')
        client = Client.objects.create(**validated_data,
                                       card=card_id,
                                       purchase_amount=purchase_amount_id)
        client_name = validated_data['name']
        bonusBalance = card['bonusBalance']
        client_email = validated_data['mail']
        create_client_messenge = (f'{client_name}, здравствуйте. '
                                  f'Спасибо за регистрацию. '
                                  f'Вам начислено {bonusBalance}. '
                                  f'Текущий баланс {bonusBalance}.')
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
        fields = ('username', 'url', 'activity',
                  'аddress', 'email', 'password',
                  'first_name', 'last_name')


class TypeCardtSerializer(serializers.ModelSerializer):
    """Cериалайзер для работы с типами карт"""

    class Meta:
        model = TypeCard
        fields = ('id', 'name', 'purchase_amount', 'initial_bonuses',
                  'rate_field',  'account',)
