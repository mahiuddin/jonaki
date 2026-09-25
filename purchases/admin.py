from django.contrib import admin
from .models import Purchase, PurchaseItem, PurchaseReturn, PurchaseReturnItem
from django.forms import TimeInput
from django.db import models


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1
    autocomplete_fields = ['product']  # Requires search_fields in ProductAdmin
    fields = [
        'product', 
        'quantity', 
        'purchase_price'
    ]

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TimeField: {
            'widget': TimeInput(
                attrs={
                    'type': 'time'
                }
            )
        }
    }
    
    list_display = [
        'purchase_number', 
        'supplier', 
        'purchase_date', 
        'gross_amount', 
        'discount', 
        'net_amount'
    ]
    inlines = [PurchaseItemInline]
    
    list_filter = ['purchase_date', 'supplier']
    search_fields = ['purchase_number', 'supplier__name', 'remarks']
    autocomplete_fields = ['supplier']  # Requires search_fields in SupplierAdmin
    date_hierarchy = 'purchase_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Purchase Information', {
            'fields': (
                ('purchase_number', 'supplier'),
                ('purchase_date', 'purchase_time')
            )
        }),
        ('Financial Details', {
            'fields': (
                ('gross_amount', 'discount', 'net_amount')
            )
        }),
        ('Additional Notes', {
            'fields': ('remarks',)
        }),
        ('System Timestamps', {
            'classes': ('collapse',),
            'fields': (('created_at', 'updated_at'),)
        }),
    )


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = [
        'purchase', 
        'product', 
        'quantity', 
        'purchase_price', 
        'net_amount'
    ]
    list_filter = ['created_at', 'product']
    search_fields = ['purchase__purchase_number', 'product__name']
    autocomplete_fields = ['purchase', 'product']
    readonly_fields = ['created_at', 'updated_at']

class PurchaseReturnItemInline(admin.TabularInline):
    model = PurchaseReturnItem
    extra = 1
    autocomplete_fields = ['product']
    readonly_fields = ['total_amount']


@admin.register(PurchaseReturn)
class PurchaseReturnAdmin(admin.ModelAdmin):
    list_display = [
        'return_number',
        'supplier',
        'return_date',
        'total_amount',
        'created_at',
    ]
    list_filter = ['return_date', 'supplier']
    search_fields = ['return_number', 'supplier__name', 'remarks']
    autocomplete_fields = ['supplier']
    readonly_fields = ['total_amount']
    inlines = [PurchaseReturnItemInline]
    date_hierarchy = 'return_date'