from django.urls import path,include


app_name = 'accounts'

urlpatterns = [
    path("api/V1/",include('accounts.api.V1.urls'))
]