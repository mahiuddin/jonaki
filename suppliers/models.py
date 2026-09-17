from django.db import models
from django.db.models import Sum
from django.utils import timezone
from common.constants import DISTRICT_CHOICES, PAYMENT_METHOD_CHOICES
from jonakimachinerystore import settings


class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(
        max_length=50, choices=DISTRICT_CHOICES, blank=True, null=True
    )
    area = models.CharField(max_length=100, blank=True, null=True)

    # Live running balance (Payable to Supplier)
    due_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        editable=False,
        help_text="Live current due owed to supplier",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Due: ৳{self.due_amount})"


class SupplierPayment(models.Model):
    payment_date = models.DateField(default=timezone.now)

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='CASH'
    )

    reference_no = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Cheque No / Transaction ID / Receipt Reference"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-payment_date', '-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['supplier', 'payment_date', 'amount'],
                name='unique_supplier_payment_date_amount'
            )
        ]

    def __str__(self):
        return f"{self.supplier.name} - {self.amount} ({self.payment_date})"