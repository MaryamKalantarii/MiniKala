from django.urls import include, path
from .views import CustomerDashboardView, CustomerOrderDetailView, CustomerOrderListView,CustomerProfileView, UserAddressViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('addresses', UserAddressViewSet, basename='user-address')
urlpatterns = [
    path('home/', CustomerDashboardView.as_view(), name='customer-home'),
    path('profile/', CustomerProfileView.as_view(), name='profile'),
    path('orders/', CustomerOrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', CustomerOrderDetailView.as_view(), name='order-detail'),
    path('', include(router.urls)),
]
