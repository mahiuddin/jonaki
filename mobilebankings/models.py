from datetime import timezone
from django.db import models

from accounts.models import Employee
from common.constants import INVEST_TYPE_CHOICES, MOBILE_BANKING_CATEGORY_CHOICES
from finances.models import ExpenseType

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
    

class MobileBankingExpense(models.Model):
    expense_date = models.DateField()

    expense_type = models.ForeignKey(
        ExpenseType,
        on_delete=models.PROTECT,
        related_name='mobilebankingexpenses'
    )

    amount = models.IntegerField(
        help_text="Expense amount"
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['expense_date', 'expense_type','amount'],
                name='unique_expense_date_expense_type_amount'
            )
        ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.expense_type.name} - {self.amount} ({self.expense_date})"


class MobileBankingProfitShare(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='mobile_banking_profit_shares'
    )

    profit_sharing_date = models.DateField()

    amount = models.IntegerField(
        help_text="Profit sharing amount"
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['profit_sharing_date', 'employee'],
                name='unique_profit_sharing_date_employee'
            )
        ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.name} - {self.profit_sharing_date} - {self.amount}"

class MobileBankingInvest(models.Model):
    invest_date = models.DateField()
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='mobile_banking_invests'
    )

    invest_type = models.CharField(
        max_length=100,
        choices=INVEST_TYPE_CHOICES
    )

    amount = models.IntegerField(
        help_text="Expense amount"
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['invest_date','employee','invest_type'],
                name='unique_invest_date_employee_invest_type'
            )
        ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.name} - {self.amount} ({self.invest_date})"    