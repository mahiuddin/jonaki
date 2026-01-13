from django.contrib import admin

from mobilebankings.models import MobileBankingExpense, MobileBankingProfit

# Register your models here.
@admin.register(MobileBankingProfit)
class MobileBankingProfitAdmin(admin.ModelAdmin):
    list_display = ('mobile_banking_category', 'profit_amount', 'profit_date')
    list_filter = ('mobile_banking_category', 'profit_date')
    date_hierarchy = 'profit_date'

class Meta:
    unique_together = ('profit_date', 'mobile_banking_category')

@admin.register(MobileBankingExpense)
class MobileBankingExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'expense_date',
        'expense_type',
        'amount',
        'description',
        'created_at',
        'updated_at'
    )
    search_fields = ('expense_date', 'expense_type', 'description')
    list_filter = ('expense_date', 'expense_type', 'amount')    