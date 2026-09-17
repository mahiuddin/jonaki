from django.contrib import admin

from .models import CustomerReconciliation, FinancialReconciliation, ProductReconciliation, StockAdjustment, StockMovement, SupplierReconciliation

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

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = [
        'created_at',
        'product',
        'movement_type',
        'quantity',
        'reference_number',
    ]
    list_filter = ['movement_type', 'created_at']
    search_fields = ['product__name', 'product__sku', 'reference_number']
    autocomplete_fields = ['product']
    date_hierarchy = 'created_at'

    # Prevent manual edits/deletions to preserve strict audit trails
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'product', 'reason', 'quantity', 'remarks', 'adjustment_date']
    list_filter = ['reason', 'created_at']
    search_fields = ['product__name', 'product__sku', 'remarks']
    autocomplete_fields = ['product']
    date_hierarchy = 'created_at'