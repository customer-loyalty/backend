from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import *
CHOICES = (('male', 'Мужской пол'), ('female', 'Женский пол'))
PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

class TypeCard(models.Model):
    """Класс для работы с типом карт"""
    name = models.CharField(
        verbose_name='Имя',
        help_text='Введите свое имя',
        max_length=150
    )
    purchase_amount = models.PositiveIntegerField(default=0,
        verbose_name='Сумма покупки')
    rate_field = models.DecimalField(max_digits=3, decimal_places=0, 
                                     default=Decimal('0'),
                                     validators=PERCENTAGE_VALIDATOR,
                                     verbose_name='Процент скидки')
    account = models.ForeignKey(
        'Account',
        null=True,
        on_delete=models.CASCADE,
        verbose_name='аккаунт',
    )

class Сard(models.Model):
    """Класс для работы с моделью карты клиента (покупателя)"""
    cardType = models.ForeignKey(
        TypeCard,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Тип карты',
    )
    cardId =  models.IntegerField(verbose_name='Код карты', unique=True)
                                 
    bonusBalance =  models.PositiveIntegerField(default=0,
        verbose_name='Баланс карты'
    )


    
    
class PurchaseAmount(models.Model):
    """Класс для работы с моделью общей стоимостью покупок"""
    total_amount = models.PositiveIntegerField(
            verbose_name='Сумма покупок'
        )
    card = models.ForeignKey(
        Сard,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Карта клиента',
    )
    

class Account(AbstractUser):
    """Класс для работы с модель Аккаунт(компания)"""

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    username = models.CharField(
        db_index=True,
        max_length=150,
        unique=True,
        verbose_name='Уникальное имя',
        validators=[AbstractUser.username_validator, ],)
    phone_number = PhoneNumberField()
    email = models.EmailField('электронный адрес', max_length=254, unique=True)
    
    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ['id']

    def __str__(self):
        return self.username


class Client(models.Model):
    """Класс для работы с моделью Клиент(покупатель)"""
    name = models.CharField(
        verbose_name='Имя',
        help_text='Введите свое имя',
        max_length=150
    )
    surname= models.CharField(
        verbose_name='Фамилия',
        help_text='Введите свою фамилию',
        max_length=150
    )
    middleName = models.CharField(
        verbose_name='Отчество',
        help_text='Введите свое отчество',
        max_length=150)
    birthday = models.DateField(max_length=8)
    gender = models.CharField(choices=CHOICES,
                           default="Мужской пол",
                           max_length=40)
    reg = models.DateTimeField(auto_now_add=True)
    telegram = models.CharField(
        verbose_name='имя аккаунта телеграмм',
        max_length=150
    )
    phone_number = PhoneNumberField()
    client = models.ForeignKey(
        'Account',
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Компания',
    )
    card = models.ForeignKey(
        Сard,
        on_delete=models.CASCADE,
        verbose_name='Карта',
    )
    purchase_amount = models.ForeignKey(
        'PurchaseAmount',
        on_delete=models.CASCADE,
        verbose_name='Карта',
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.name} {self.surname}'
    

    

