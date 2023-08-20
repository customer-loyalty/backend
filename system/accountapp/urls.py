from rest_framework.routers import DefaultRouter
from django.urls import include, path

from accountapp.views import ClientViewSet


app_name = 'api'


router = DefaultRouter()
router.register('',  ClientViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
