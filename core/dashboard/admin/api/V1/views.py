from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.admin import CustomeUser
from products.api.V1.serializers import ProductSerializer
from products.models import ProductModel
from dashboard.api.V1.permissions import IsAdminUserType
from order.models import CouponModel
from .serializers import CouponSerializer,AdminProfileSerializer,UserSerializer
from rest_framework import status,viewsets
from rest_framework.generics import RetrieveUpdateAPIView 

class AdminDashboardView(APIView):
    permission_classes = [IsAdminUserType]

    def get(self, request):
        return Response({"message": "Welcome to admin dashboard!"})


class CouponViewSet(viewsets.ModelViewSet):
    queryset = CouponModel.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUserType]


class AdminProfileView(RetrieveUpdateAPIView):
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAdminUserType]

    def get_object(self):
        return self.request.user.user_profile

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            "message": "پروفایل با موفقیت بروزرسانی شد",
            "data": response.data
        }, status=status.HTTP_200_OK)
    

class ProductAdminView(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUserType]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserView(viewsets.ModelViewSet):
    queryset = CustomeUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUserType]