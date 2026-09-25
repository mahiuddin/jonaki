from django.contrib import admin
from django.db import models
from django.forms import TimeInput

# Register your models here.

from .models import Order, OrderItem, OrderReturn

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    autocomplete_fields = ['product']
    fields = [
        'product', 
        'quantity', 
        'sale_price'
    ]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TimeField: {
            'widget': TimeInput(
                attrs={
                    'type': 'time'
                }
            )
        }
    }
    list_display = (
        'memo_number',
        'order_date',
        'order_time',
        'customer_id',
        'sale_amount',
        'profit',
        'status'
    )

    inlines = [OrderItemInline]

    list_filter = ('status', 'order_date', 'order_time')
    search_fields = ('memo_number','customer_id__name')

@admin.register(OrderReturn)
class OrderReturnAdmin(admin.ModelAdmin):
    list_display = [
        'return_date',
        'order',
        'product',
        'quantity',
        'unit_price',
        'total_amount',
        'remarks',
    ]
    list_filter = ['return_date', 'created_at']
    
    # 2. Replaces dropdown with a search input for Order and Product
    autocomplete_fields = ['order', 'product']
    
    readonly_fields = ['total_amount']
    date_hierarchy = 'return_date'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'product')
