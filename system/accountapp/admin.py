from django.contrib import admin

from accountapp.models import (Сard, Account, Client, Owner)                   


@admin.register(Сard)
class СardAdmin(admin.ModelAdmin):
    pass


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    pass
