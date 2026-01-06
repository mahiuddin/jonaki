from django.contrib import admin

from mobilebankings.models import MobileBankingProfit

# Register your models here.
@admin.register(MobileBankingProfit)
class MobileBankingProfitAdmin(admin.ModelAdmin):
    list_display = ('mobile_banking_category', 'profit_amount', 'profit_date')
    list_filter = ('mobile_banking_category', 'profit_date')
    date_hierarchy = 'profit_date'

class Meta:
    unique_together = ('profit_date', 'mobile_banking_category')