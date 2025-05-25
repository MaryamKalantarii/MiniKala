from rest_framework.views import APIView
from rest_framework.response import Response
from dashboard.api.V1.permissions import IsCustomerUserType

class CustomerDashboardView(APIView):
    permission_classes = [IsCustomerUserType]

    def get(self, request):
        return Response({"message": "Welcome to customer dashboard!"})
