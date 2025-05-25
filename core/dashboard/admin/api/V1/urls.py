from django.urls import path
from .views import AdminDashboardView

urlpatterns = [
    path('home/', AdminDashboardView.as_view(), name='admin-home'),
]
