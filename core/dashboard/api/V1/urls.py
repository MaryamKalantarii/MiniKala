from django.urls import path
from .views import WhoAmIView

urlpatterns = [
    path('whoami/', WhoAmIView.as_view(), name='whoami'),
]
