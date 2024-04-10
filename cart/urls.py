from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('', views.CartItemViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]


""" get /cart/   =====> all cartitems

delete /cart/ ======> clear cart

post /cart/ ======> add to cart

get /cart/{id} ======> get cartitem by id

update /cart/{id} ======> update cartitem by id """
