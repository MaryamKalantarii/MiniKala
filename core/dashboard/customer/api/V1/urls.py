from django.urls import path
from .views import CustomerDashboardView

urlpatterns = [
    path('home/', CustomerDashboardView.as_view(), name='customer-home'),
]
