from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions
from order.models import OrderModel
from .serializers import OrderCreateSerializer,OrderSerializer

class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response({"detail": "سفارش با موفقیت ثبت شد.", "order_id": order.id}, status=status.HTTP_201_CREATED)

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Handles listing and retrieving user orders.

    - list: Display the list of user orders
    - retrieve: View specific order details
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user)