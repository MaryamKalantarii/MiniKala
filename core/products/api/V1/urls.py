from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter

app_name = 'api-v1'

router = DefaultRouter()
router.register('products', ProductView, basename='products')
urlpatterns = router.urls
