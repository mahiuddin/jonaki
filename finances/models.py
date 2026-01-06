from django.db import models

# Create your models here.
class ExpenseType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Expense(models.Model):
    expense_date = models.DateField()

    expense_type = models.ForeignKey(
        ExpenseType,
        on_delete=models.PROTECT,
        related_name='expenses'
    )

    amount = models.IntegerField(
        help_text="Expense amount"
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.expense_type.name} - {self.amount} ({self.expense_date})"