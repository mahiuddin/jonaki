from django.db import models
from django.utils import timezone
from common.constants import FINANCIAL_RECONCILIATION_CATEGORY_CHOICES, MOVEMENT_TYPE_DAMAGE, MOVEMENT_TYPES
from suppliers.models import Supplier
from products.models import Product
from customers.models import Customer


class CustomerReconciliation(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='reconciliations'
    )

    updated_amount = models.IntegerField(
        help_text="Final receivable balance after reconciliation"
    )

    adjust_amount = models.IntegerField(
        help_text="Adjustment amount (+ / -)"
    )

    reconciliation_date = models.DateField(default=timezone.now)

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.name} | Adjust: {self.adjust_amount}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'reconciliation_date','updated_amount'], 
                name='unique_customer_reconciliation_date_updated_amount'
            )
        ]


class ProductReconciliation(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reconciliations'
    )

    physical_stock_quantity = models.IntegerField(
        help_text="Physical stock quantity at reconciliation"
    )

    adjust_quantity = models.IntegerField(
        help_text="Adjustment quantity (+ / -)"
    )

    reconciliation_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        help_text="Price used for reconciliation valuation"
    )

    reconciliation_date = models.DateField(default=timezone.now)

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} | Adjust {self.adjust_quantity}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'reconciliation_date','physical_stock_quantity'], 
                name='unique_product_reconciliation_date_physical_stock_quantity'
            )
        ]
    

class SupplierReconciliation(models.Model):
    
    reconciliation_date = models.DateField(default=timezone.now)
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='reconciliations'
    )

    balance_amount = models.IntegerField(
        help_text="Final supplier balance after reconciliation"
    )

    adjust_amount = models.IntegerField(
        default=0,
        help_text="Adjustment amount (+ / -)"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.supplier.name} | Adjust: {self.adjust_amount}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['supplier', 'reconciliation_date','balance_amount'], 
                name='unique_supplier_reconciliation_date_balance'
            )
        ]

class FinancialReconciliation(models.Model):
    category = models.CharField(
        max_length=10, 
        choices=FINANCIAL_RECONCILIATION_CATEGORY_CHOICES,
    )
    account_name = models.CharField(max_length=100)
    reconciliation_date = models.DateField(default=timezone.now)
    
    # Amount as an integer
    amount = models.IntegerField()
    
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['account_name', 'reconciliation_date'], 
                name='unique_account_daily_recon_v3'
            )
        ]

    def __str__(self):
        return f"{self.account_name} - {self.reconciliation_date}"

class StockMovement(models.Model):
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name='stock_movements'
    )
    quantity = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        help_text="Positive number for IN, negative for OUT."
    )
    
    # Using TextChoices:
    movement_type = models.CharField(
        max_length=30, 
        choices=MOVEMENT_TYPES
    )

    movement_date = models.DateField(default=timezone.now)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Stock Movement"
        verbose_name_plural = "Stock Movements"

    def __str__(self):
        return f"{self.product.name} | {self.get_movement_type_display()} | {self.quantity}"

class StockAdjustment(models.Model):
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name='adjustments'
    )
    quantity = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        help_text="Enter quantity to adjust. Damaged/Lost will automatically reduce stock."
    )
    reason = models.CharField(
        max_length=30, 
        choices=MOVEMENT_TYPES,
        default=MOVEMENT_TYPE_DAMAGE
    )
    remarks = models.TextField(
        blank=True, 
        null=True,
        help_text="Provide details (e.g. Broken during transit, missing after inventory count)"
    )

    adjustment_date = models.DateField(
        default=timezone.now,
        help_text="The date the damage or loss occurred."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Stock Adjustment"
        verbose_name_plural = "Stock Adjustments"

    def __str__(self):
        return f"{self.product.name} - {self.get_reason_display()} ({self.quantity})"