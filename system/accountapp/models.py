from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Сard(models.Model):
    name = models.CharField(
        verbose_name='Имя',
        help_text='Имя карты',
        max_length=150
    )
    bonus_rules = models.CharField(
        verbose_name='бонусы',
        max_length=150
    )
    balance = models.CharField(
        verbose_name='баланс',
        max_length=150
    )


class Account(AbstractUser):
    """Класс для работы с модель """

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    username = models.CharField(
        db_index=True,
        max_length=150,
        unique=True,
        verbose_name='Уникальное имя',
        validators=[AbstractUser.username_validator, ],)
    email = models.EmailField('электронный адрес', max_length=254, unique=True)
    client = models.ForeignKey(
        'Client',
        null = True,
        on_delete=models.CASCADE,
        #related_name='client',
        verbose_name='Клиент',
    )
    card = models.ForeignKey(
        Сard,
        null = True,
        on_delete=models.CASCADE,
        verbose_name='Карта',
    )
    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ['id']

    def __str__(self):
        return self.username

class Client(models.Model):
    first_name = models.CharField(
        verbose_name='Имя',
        help_text='Введите свое имя',
        max_length=150
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        help_text='Введите свою фамилию',
        max_length=150
    )
    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name='Телефонный номер',
        help_text='Введите Ваш телефонный номер'
    )
    card = models.ForeignKey(
        Сard,
        on_delete=models.CASCADE,
        verbose_name='Карта',
    )

    class Meta:
        verbose_name = 'Клиент'

        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

