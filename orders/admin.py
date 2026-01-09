from django.contrib import admin
from django.db import models
from django.forms import TimeInput

# Register your models here.

from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    autocomplete_fields = ['product']

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
        'status'
    )

    inlines = [OrderItemInline]

    list_filter = ('status', 'order_date', 'order_time')
    search_fields = ('memo_number','customer_id__name')
