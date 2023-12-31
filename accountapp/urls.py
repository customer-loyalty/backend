from rest_framework.routers import DefaultRouter
from django.urls import include, path

from accountapp.views import (ClientViewSet, AccountViewSet,
                              TypeCardViewSet, PurchaseAmountViewSet,
                              CardBonusViewSet)


app_name = 'api'


router = DefaultRouter()
router.register('client',  ClientViewSet, basename='client')
router.register('bonus',  CardBonusViewSet, basename='bonus')
router.register('users', AccountViewSet, basename='users')
router.register('cardtype', TypeCardViewSet, basename='cardtype')
router.register('purchase', PurchaseAmountViewSet, basename='purchase')
urlpatterns = [
    path('', include(router.urls))
]
