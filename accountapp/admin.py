from django.contrib import admin

from accountapp.models import (Сard, PurchaseAmount, Account, Client, TypeCard)                   


@admin.register(Сard)
class СardAdmin(admin.ModelAdmin):
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
