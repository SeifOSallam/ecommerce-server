from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('',views.CartViewSet)
router.register('item/cartitem',views.CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
