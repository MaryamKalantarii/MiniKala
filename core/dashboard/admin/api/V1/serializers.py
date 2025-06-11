from rest_framework import serializers
from order.models import CouponModel
from accounts.models import Profile,CustomUser


class CouponSerializer(serializers.ModelSerializer):
    used_by = serializers.PrimaryKeyRelatedField(read_only=True, many=True)  # فقط نمایش آی‌دی‌ها

    class Meta:
        model = CouponModel
        fields = [
            'id',
            'code',
            'discount_percent',
            'max_limit_usage',
            'used_by',
            'expiration_date',
            'created_date',
            'updated_date',
        ]
        read_only_fields = ['created_date', 'updated_date', 'used_by']

class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number','image']




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
    
        fields = [
            "email",
            "is_active",
            "is_verified",
        ]
         