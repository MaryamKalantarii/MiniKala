from rest_framework import viewsets,filters
from .serializers import ProductSerializer,CategorySerializer
from ...models import ProductModel,ProductCategoryModel,ProductStatusType
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .permisstions import IsAdminAndVerifiedOrReadOnly
class ProductView(viewsets.ModelViewSet):
    
    permission_class = [IsAdminAndVerifiedOrReadOnly]
    serializer_class = ProductSerializer
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['description', 'category__title']
    ordering_fields = ['created_date', 'price']
    ordering = ['-created_date']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)