from rest_framework.routers import DefaultRouter
from django.urls import include, path

from accountapp.views import ClientViewSet, AccountViewSet


app_name = 'api'


router = DefaultRouter()
router.register('card',  ClientViewSet, basename='')
router.register('users', AccountViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
