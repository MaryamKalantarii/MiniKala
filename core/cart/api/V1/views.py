from rest_framework import viewsets, permissions
from ...models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import ProductModel

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        product = serializer.validated_data['product_id']
        product_instance = ProductModel.objects.get(id=product)

        # اگر محصول قبلاً تو سبد بود، فقط مقدار رو زیاد می‌کنیم
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product_instance,
            defaults={'quantity': serializer.validated_data.get('quantity', 1)}
        )
        if not created:
            item.quantity += serializer.validated_data.get('quantity', 1)
            item.save()
        serializer.instance = item
