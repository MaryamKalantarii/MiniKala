from django.db import models
from django.db import models
from products.models import ProductModel  

class Cart(models.Model):
    user = models.OneToOneField('accounts.CustomeUser', on_delete=models.CASCADE, related_name='cart')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.email}"

    @property
    def total(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    @property
    def total_price(self):
        return self.quantity * self.product.get_price()
