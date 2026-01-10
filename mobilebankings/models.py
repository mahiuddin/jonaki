from datetime import timezone
from django.db import models

from common.constants import MOBILE_BANKING_CATEGORY_CHOICES

# Create your models here.
class MobileBankingProfit(models.Model):

    profit_date = models.DateField()
    mobile_banking_category = models.CharField(
        max_length=20,
        choices=MOBILE_BANKING_CATEGORY_CHOICES
    )

    profit_amount = models.IntegerField(
        help_text="Profit earned from mobile banking"
    )

    remarks = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes or remarks"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['profit_date', 'mobile_banking_category'],
                name='unique_profit_date_mobile_banking_category'
            )
        ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_mobile_banking_category_display()} - {self.profit_amount} ({self.profit_date})"