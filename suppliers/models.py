from django.db import models
from django.utils import timezone
from common.constants import DISTRICT_CHOICES
from jonakimachinerystore import settings

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)

    contact_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    contact_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    district = models.CharField(
        max_length=50,
        choices=DISTRICT_CHOICES,
        blank=True,
        null=True
    )

    area = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SupplierPayment(models.Model):
    payment_date = models.DateField()

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['supplier', 'payment_date', 'amount'],
                name='unique_supplier_payment_date_amount'
            )
        ]

    def __str__(self):
        return f"{self.supplier.name} - {self.amount} ({self.payment_date})"