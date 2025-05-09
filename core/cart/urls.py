from django.urls import path,include


app_name = 'cart'

urlpatterns = [
    path("api/V1/",include('cart.api.V1.urls'))
]