from django.urls import path
from .views import RegistrationView,IsVerifiedView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name='api-v1-accounts'

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path("is-verified/<str:token>", IsVerifiedView.as_view(), name="is-verified"),
    #simplejwt
    path('token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]