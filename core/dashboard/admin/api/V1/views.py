from rest_framework.views import APIView
from rest_framework.response import Response
from dashboard.api.V1.permissions import IsAdminUserType

class AdminDashboardView(APIView):
    permission_classes = [IsAdminUserType]

    def get(self, request):
        return Response({"message": "Welcome to admin dashboard!"})
