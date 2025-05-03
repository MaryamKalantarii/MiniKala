from rest_framework import viewsets
from .serializer import ProductSerializer,CategorySerializer
from ...models import ProductModel,ProductCategoryModel,ProductStatusType


class ProductView(viewsets.ModelViewSet):

    class_serializer = ProductSerializer
    queryset = ProductModel.objects.filter(
        status=ProductStatusType.publish.value)
    