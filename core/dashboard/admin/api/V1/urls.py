from django.urls import path,include
from .views import AdminDashboardView,CouponViewSet, ProductAdminView,UserView
from rest_framework.routers import DefaultRouter
from .views import CouponViewSet

router = DefaultRouter()
router.register('admin/coupons', CouponViewSet, basename='coupon')
router.register('admin/products', ProductAdminView, basename='admin-products')
router.register('admin/users', UserView, basename='users')

urlpatterns = [
    path('home/', AdminDashboardView.as_view(), name='admin-home'),
    path('api/', include(router.urls)),
]
