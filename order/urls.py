from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('',views.OrderViewSet)
router.register('item/orderitem',views.OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<pk>/cancel', 
        views.OrderViewSet.as_view({'post': 'cancel_order'}), name='cancel_order'),
]
