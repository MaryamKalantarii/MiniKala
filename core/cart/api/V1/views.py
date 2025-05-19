from rest_framework import viewsets, permissions
from ...models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer,CartItemCreateSerializer
from products.models import ProductModel
from rest_framework.decorators import action
from rest_framework.response import Response

class CartViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing the authenticated user's shopping cart.

    Actions:
        - list: Return a list of carts belonging to the current user (usually one).
        - retrieve: Return details of a specific cart.
        - create: Create a new cart for the authenticated user.
        - update/partial_update: Modify the user's cart.
        - destroy: Delete the user's cart.
        - me: [GET] Return the current authenticated user's cart, creating one if it doesn't exist.
    """
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Retrieve the authenticated user's cart.
        Creates one if it doesn't exist.

        Returns:
            200 OK with serialized Cart object.
        """
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def get_queryset(self):
        """
        Restrict the queryset to carts owned by the authenticated user only.
        """
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically assign the authenticated user to the created cart.
        """
        serializer.save(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing items inside the authenticated user's cart.

    Actions:
        - list: List all items in the user's cart.
        - retrieve: Return a specific item in the cart.
        - create: Add a product to the cart (or increase quantity if already exists).
        - update/partial_update: Modify quantity of a specific item.
        - destroy: Remove an item from the cart.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter cart items to only include items belonging to the current user's cart.
        """
        return CartItem.objects.filter(cart__user=self.request.user)

    def get_serializer_class(self):
        """
        Use different serializer for create action to accept simple product_id and quantity.
        """
        if self.action == 'create':
            return CartItemCreateSerializer
        return CartItemSerializer

    def create(self, request, *args, **kwargs):
        """
        Add a product to the user's cart. If the product already exists in the cart,
        increase the quantity. Automatically creates a cart if the user doesn't have one.

        Expected JSON:
            {
                "product_id": int,
                "quantity": int
            }

        Returns:
            201 Created with the updated CartItem
            400 Bad Request if product is invalid
        """
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data.get('quantity', 1)

        try:
            product = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            return Response({'product_id': 'The desired product was not found.'}, status=status.HTTP_400_BAD_REQUEST)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()

        output_serializer = CartItemSerializer(item)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
