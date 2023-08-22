from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


CHOICES = (('male', 'Мужской пол'), ('female', 'Женский пол'))


class Сard(models.Model):
    cardType = models.CharField(
        verbose_name='Имя',
        help_text='Тип карты',
        max_length=150
    )
    cardId =  models.IntegerField(max_length=16, 
                                  verbose_name='Код карты')
    bonusBalance = models.CharField(
        verbose_name='Баланс карты',
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
    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name='Телефонный номер',
        help_text='Введите Ваш телефонный номер'),
    email = models.EmailField('электронный адрес', max_length=254, unique=True)
    website = models.URLField(max_length=250)
    address = models.CharField(
        verbose_name='Адрес организации',
        max_length=150
    )
    owner = models.ForeignKey(
        'Owner',
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
    )

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ['id']

    def __str__(self):
        return self.username


class Client(models.Model):
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
    phone = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name='Телефонный номер',
        help_text='Введите Ваш телефонный номер'
    )
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

    class Meta:
        verbose_name = 'Клиент'

        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.name} {self.surname}'
    

class Owner(models.Model):
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
