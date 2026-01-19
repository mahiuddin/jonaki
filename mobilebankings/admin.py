from django.contrib import admin

from mobilebankings.models import MobileBankingExpense, MobileBankingInvest, MobileBankingProfit, MobileBankingProfitShare

# Register your models here.
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

@admin.register(MobileBankingProfitShare)
class MobileBankingProfitShareAdmin(admin.ModelAdmin):
    list_display = (
        'profit_sharing_date',
        'employee',
        'amount',
        'description',
        'created_at',
        'updated_at'
    )
    search_fields = ('profit_sharing_date', 'employee', 'description')
    list_filter = ('profit_sharing_date', 'employee', 'amount')  
         
@admin.register(MobileBankingInvest)
class MobileBankingInvestAdmin(admin.ModelAdmin):
    list_display = (
        'invest_date',
        'employee',
        'invest_type',
        'amount',
        'description',
        'created_at',
        'updated_at'
    )
    search_fields = ('invest_date', 'employee', 'invest_type', 'description')
    list_filter = ('invest_date', 'employee', 'invest_type', 'amount')  

@admin.register(MobileBankingProfit)
class MobileBankingProfitAdmin(admin.ModelAdmin):
    list_display = ('mobile_banking_category', 'profit_amount', 'profit_date')
    list_filter = ('mobile_banking_category', 'profit_date')
    date_hierarchy = 'profit_date'

class Meta:
    unique_together = ('profit_date', 'mobile_banking_category')