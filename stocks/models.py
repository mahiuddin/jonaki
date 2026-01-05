from django.db import models
from django.utils import timezone
from suppliers.models import Supplier


class SupplierReconciliation(models.Model):
    
    reconciliation_date = models.DateField()
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='reconciliations'
    )

    balance_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        help_text="Final supplier balance after reconciliation"
    )

    adjust_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        blank=True,
        null=True,
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