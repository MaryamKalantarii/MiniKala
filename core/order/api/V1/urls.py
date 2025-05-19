# orders/api/v1/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderCreateAPIView

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('orders/create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('', include(router.urls)),
]
