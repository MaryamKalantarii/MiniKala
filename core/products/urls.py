from django.urls import path,include


app_name = 'products'

urlpatterns = [
    path("api/V1/",include('products.api.V1.urls'))
]