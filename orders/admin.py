from django.contrib import admin

# Register your models here.

from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'memo_number',
        'order_date',
        'order_time',
        'customer_id',
        'sale_amount',
        'status'
    )
    list_filter = ('status', 'order_date', 'order_time')
    search_fields = ('memo_number','customer_id__name')
