# Generated by Django 4.2.4 on 2023-08-21 17:38

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(db_index=True, max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Уникальное имя')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='электронный адрес')),
                ('website', models.URLField(max_length=250)),
                ('address', models.CharField(max_length=150, verbose_name='Адрес организации')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'Аккаунт',
                'verbose_name_plural': 'Аккаунты',
                'ordering': ['id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Введите свое имя', max_length=150, verbose_name='Имя')),
                ('last_name', models.CharField(help_text='Введите свою фамилию', max_length=150, verbose_name='Фамилия')),
            ],
        ),
        migrations.CreateModel(
            name='Сard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Имя карты', max_length=150, verbose_name='Имя')),
                ('bonus_rules', models.CharField(max_length=150, verbose_name='бонусы')),
                ('cardId', models.IntegerField(help_text='Enter field documentation', max_length=16)),
                ('balance', models.CharField(max_length=150, verbose_name='баланс')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Введите свое имя', max_length=150, verbose_name='Имя')),
                ('last_name', models.CharField(help_text='Введите свою фамилию', max_length=150, verbose_name='Фамилия')),
                ('patronymic1', models.CharField(help_text='Введите свое отчество', max_length=150, verbose_name='Отчество')),
                ('dob', models.DateField(max_length=8)),
                ('sex', models.CharField(choices=[('male', 'Мужской пол'), ('female', 'Женский пол')], default='Мужской пол', max_length=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('telegram', models.CharField(max_length=150, verbose_name='имя аккаунта телеграмм')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Введите Ваш телефонный номер', max_length=128, null=True, region=None, verbose_name='Телефонный номер')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountapp.сard', verbose_name='Карта')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.AddField(
            model_name='account',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accountapp.owner', verbose_name='Владелец'),
        ),
        migrations.AddField(
            model_name='account',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
