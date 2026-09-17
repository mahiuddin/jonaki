from django.db import models
from django.utils import timezone

from customers.models import Customer
from common.constants import ORDER_STATUS_CHOICES
from products.models import Product

# Create your models here.

class Order(models.Model):
    order_date = models.DateField()
    order_time = models.TimeField()

    memo_number = models.CharField(
        max_length=100,
        unique=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='orders'
    )

    gross_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    sale_amount = models.IntegerField(
        help_text="Sale amount"
    )

    profit = models.IntegerField(
        help_text="Profit amount"
    )

    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='complete'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order_date', 'memo_number', 'sale_amount'],
                name='unique_order_date_memo_number_sale_amount'
            )
        ]

    def __str__(self):
        return self.memo_number
    
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField()

    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    gross_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.memo_number} - {self.product}"

# orders/models.py
from django.db import models
from django.utils import timezone

class OrderReturn(models.Model):
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.PROTECT,
        related_name='returns'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name='returns'
    )
    quantity = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        help_text="Quantity returned by customer"
    )
    unit_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        help_text="Price per unit at which the item was refunded"
    )
    total_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        editable=False,
        help_text="Auto-calculated (quantity * unit_price)"
    )
    return_date = models.DateField(default=timezone.now)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-return_date', '-created_at']
        verbose_name = "Order Return"
        verbose_name_plural = "Order Returns"

    def save(self, *args, **kwargs):
        # Auto-calculate total return value before saving
        self.total_amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Return #{self.id} | Order: {self.order.memo_number} | Amount: {self.total_amount}"