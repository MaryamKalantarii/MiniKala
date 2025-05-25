from django.urls import path, include

urlpatterns = [
    path('admin/', include('dashboard.admin.api.V1.urls')),
    path('customer/', include('dashboard.customer.api.V1.urls')),
    path('', include('dashboard.api.V1.urls')),  # shared APIs like whoami
]
