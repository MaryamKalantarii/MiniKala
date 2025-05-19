from django.urls import path,include


app_name = 'order'

urlpatterns = [
    path("api/V1/",include('order.api.V1.urls'))
]