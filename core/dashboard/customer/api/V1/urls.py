from django.urls import path
from .views import CustomerDashboardView, CustomerOrderDetailView, CustomerOrderListView,CustomerProfileView

urlpatterns = [
    path('home/', CustomerDashboardView.as_view(), name='customer-home'),
    path('profile/', CustomerProfileView.as_view(), name='profile'),
    path('orders/', CustomerOrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', CustomerOrderDetailView.as_view(), name='order-detail'),
]
