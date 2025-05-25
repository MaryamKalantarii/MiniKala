from rest_framework.views import APIView
from rest_framework.response import Response
from dashboard.api.V1.permissions import IsCustomerUserType
from rest_framework import generics, permissions
from .serializers import CustomerProfileSerializer, OrderDetailSerializer, OrderListSerializer, UserAddressSerializer
from accounts.models import Profile
from rest_framework import status
from order.models import OrderModel, UserAddressModel
from rest_framework import viewsets

class CustomerDashboardView(APIView):
    permission_classes = [IsCustomerUserType]

    def get(self, request):
        return Response({"message": "Welcome to customer dashboard!"})




class CustomerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.user_profile

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            "message": "پروفایل با موفقیت بروزرسانی شد",
            "data": response.data
        }, status=status.HTTP_200_OK)
    
# dashboard/customer/api/V1/views/order_views.py


class CustomerOrderListView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user)


class CustomerOrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user)

class UserAddressViewSet(viewsets.ModelViewSet):
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)