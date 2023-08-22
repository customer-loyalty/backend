from rest_framework import serializers

from .models import Client, Сard

class СardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('cardType','cardId', 'bonusBalance')
        model = Сard


class ClientSerializer(serializers.ModelSerializer):
    """Класс - сериализатор модели """
    client = serializers.StringRelatedField()
    reg = serializers.DateTimeField(format="%Y-%m-%d")
    card = СardSerializer()
    class Meta:
        model = Client
        fields = ('id','name', 'surname', 'middleName', 'birthday', 'gender',
                  'reg', 'telegram', 'phone', 'client', 'card')
    

    def create(self, validated_data):
        
        request = self.context.get('request', None)
        card = validated_data.pop('card')
        print(card, 1)
        #account = validated_data.pop('client')
        card = Сard.objects.create (**card)
        print(card, 2)
        card_id= Сard.objects.latest('id')
        #print(card_id, 3)
        client = Client.objects.create(**validated_data, card =card_id)
        print(4)
        return client 


