from rest_framework.permissions import BasePermission
from accounts.models import UserType

class IsAdminUserType(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == UserType.admin.value

class IsCustomerUserType(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == UserType.customer.value
