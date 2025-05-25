from rest_framework import serializers
from accounts.models import Profile
from order.api.V1.serializers import OrderItemSerializer
from order.models import OrderModel,UserAddressModel

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number','image']



class OrderListSerializer(serializers.ModelSerializer):
    status_label = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderModel
        fields = ['id', 'created_date', 'status', 'status_label', 'final_price']

    def get_status_label(self, obj):
        return obj.get_status().get("label")

    def get_final_price(self, obj):
        return obj.get_price()


class OrderDetailSerializer(OrderListSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta(OrderListSerializer.Meta):
        fields = OrderListSerializer.Meta.fields + ['order_items']

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddressModel
        fields = ['id', 'address', 'state', 'city', 'zip_code']