from django.contrib import admin

from .models import CustomerReconciliation, FinancialReconciliation, ProductReconciliation, SupplierReconciliation

# Register your models here.

@admin.register(SupplierReconciliation)
class SupplierReconciliationAdmin(admin.ModelAdmin):
    list_display = ('reconciliation_date', 'supplier', 'balance_amount', 'adjust_amount', 'created_at')
    search_fields = ('supplier__name',)
    list_filter = ('reconciliation_date','supplier',)
    date_hierarchy = 'reconciliation_date'

@admin.register(ProductReconciliation)
class ProductReconciliationAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'physical_stock_quantity',
        'adjust_quantity',
        'reconciliation_price',
        'reconciliation_date'
    )
    list_filter = ('reconciliation_date',)
    search_fields = ('product__name',)

@admin.register(CustomerReconciliation)
class CustomerReconciliationAdmin(admin.ModelAdmin):
    list_display = ('reconciliation_date','customer', 'updated_amount', 'adjust_amount', 'created_at')
    search_fields = ('customer__name',)

@admin.register(FinancialReconciliation)
class FinancialReconciliationAdmin(admin.ModelAdmin):
    list_display = ('reconciliation_date', 'account_name', 'amount')
    
    # 1. Sidebar filters for Category and Date (Standard)
    list_filter = ('category', 'reconciliation_date')
    
    # 2. Top-bar 'Specific Date' navigation
    date_hierarchy = 'reconciliation_date' 
    
    # 3. Search by account name or specific amount
    search_fields = ('account_name', 'amount', 'remarks')