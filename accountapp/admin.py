from django.contrib import admin

from accountapp.models import (Card, PurchaseAmount, Account, Client, TypeCard)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
 pass


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(TypeCard)
class TypeCardAdmin(admin.ModelAdmin):
    pass


@admin.register(PurchaseAmount)
class PurchaseAmountAdmin(admin.ModelAdmin):
    pass
