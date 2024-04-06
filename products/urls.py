from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('',views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('popular_products/', views.ProductViewSet.as_view({'get': 'popular_products'}), name='popular_products'),
    path('<pk>/review/', views.ProductViewSet.as_view({'post': 'add_review'}), name='add_review'),
]
