from django.contrib import admin

from .models import SupplierReconciliation

# Register your models here.

@admin.register(SupplierReconciliation)
class SupplierReconciliationAdmin(admin.ModelAdmin):
    list_display = ('reconciliation_date', 'supplier', 'balance_amount', 'adjust_amount', 'created_at')
    search_fields = ('supplier__name',)
    list_filter = ('reconciliation_date', 'supplier',)

