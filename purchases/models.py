from django.db import models
from django.db.models.aggregates import Sum
from django.utils import timezone


class Purchase(models.Model):
    purchase_date = models.DateField()
    purchase_time = models.TimeField()

    purchase_number = models.CharField(
        max_length=50,
        unique=True
    )

    supplier = models.ForeignKey(
        'suppliers.Supplier',
        on_delete=models.PROTECT,
        related_name='purchases'
    )

    gross_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-purchase_date', '-id']
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"

    def __str__(self):
        return self.purchase_number


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name='purchase_items'
    )

    quantity = models.PositiveIntegerField()

    purchase_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00
    )

    gross_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name = "Purchase Item"
        verbose_name_plural = "Purchase Items"

    def __str__(self):
        return f"{self.purchase.purchase_number} - {self.product.name}"

    @property
    def total_amount(self):
        return self.quantity * self.purchase_price

class PurchaseReturn(models.Model):
    """Master Header: Supplier Return Memo / Debit Note."""

    return_number = models.CharField(
        max_length=100,
        default="Unavailable",
        unique=True,
        blank=True,
        help_text='Return Reference / Debit Note No (e.g. PRET-2026-001)',
    )
    supplier = models.ForeignKey(
        'suppliers.Supplier',
        on_delete=models.PROTECT,
        related_name='purchase_returns',
    )
    return_date = models.DateField(default=timezone.now)
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, editable=False
    )
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-return_date', '-created_at']
        verbose_name = 'Purchase Return'
        verbose_name_plural = 'Purchase Returns'

    def update_total_amount(self):
        """Recalculates total header amount from line items."""
        total = (
            self.items.aggregate(total=Sum('total_amount'))['total'] or 0.00
        )
        self.total_amount = total
        self.save(update_fields=['total_amount'])

    def __str__(self):
        return f'{self.return_number} - {self.supplier.name} ({self.total_amount})'


class PurchaseReturnItem(models.Model):
    """Child Line Item: Individual products returned."""

    purchase_return = models.ForeignKey(
        PurchaseReturn, on_delete=models.CASCADE, related_name='items'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name='purchase_return_items',
    )
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, editable=False
    )
    remarks = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.purchase_return.update_total_amount()

    def delete(self, *args, **kwargs):
        purchase_return = self.purchase_return
        super().delete(*args, **kwargs)
        purchase_return.update_total_amount()

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'