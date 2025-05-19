from rest_framework import serializers
from cart.models import Cart, CartItem
from order.models import OrderModel, OrderItemModel, UserAddressModel, CouponModel
from products.models import ProductModel
from products.api.V1.serializers import ProductSerializer
from pytz import timezone

class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemModel
        fields = ['product', 'quantity', 'price']


class OrderCreateSerializer(serializers.ModelSerializer):
    address_id = serializers.IntegerField(write_only=True)
    coupon_code = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = OrderModel
        fields = ['address_id', 'coupon_code']

    def validate_address_id(self, value):
        user = self.context['request'].user
        try:
            address = UserAddressModel.objects.get(id=value, user=user)
        except UserAddressModel.DoesNotExist:
            raise serializers.ValidationError("آدرس معتبر نیست.")
        return value

    def validate_coupon_code(self, value):
        if value:
            try:
                coupon = CouponModel.objects.get(code=value)
                if coupon.expiration_date and coupon.expiration_date < timezone.now():
                    raise serializers.ValidationError("کد تخفیف منقضی شده است.")
                return value
            except CouponModel.DoesNotExist:
                raise serializers.ValidationError("کد تخفیف پیدا نشد.")
        return value

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        cart = Cart.objects.prefetch_related('items__product').get(user=user)
        cart_items = cart.items.all()

        if not cart_items:
            raise serializers.ValidationError("سبد خرید شما خالی است.")

        # Get address
        address_obj = UserAddressModel.objects.get(id=validated_data['address_id'], user=user)

        # Handle coupon
        coupon = None
        if validated_data.get('coupon_code'):
            coupon = CouponModel.objects.get(code=validated_data['coupon_code'])

        # Calculate total
        total_price = sum(item.product.get_price() * item.quantity for item in cart_items)

        # Create order
        order = OrderModel.objects.create(
            user=user,
            address=address_obj.address,
            state=address_obj.state,
            city=address_obj.city,
            zip_code=address_obj.zip_code,
            total_price=total_price,
            coupon=coupon
        )

        # Create order items
        for item in cart_items:
            OrderItemModel.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price()
            )

        # Clear cart
        cart.items.all().delete()

        # Mark coupon as used
        if coupon:
            coupon.used_by.add(user)

        return order


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItemModel
        fields = ['id', 'product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderModel
        fields = ['id', 'order_items', 'total_price', 'final_price', 'status', 'status_display',
                  'address', 'state', 'city', 'zip_code', 'created_date']

    def get_status_display(self, obj):
        return obj.get_status()

    def get_final_price(self, obj):
        return obj.get_price()