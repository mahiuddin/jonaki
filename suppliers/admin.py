from django.contrib import admin
from .models import Supplier, SupplierPayment

# Register your models here.
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'contact_name',
        'contact_number',
        'district',
        'area',
        'created_at'
    )
    search_fields = ('name', 'contact_name', 'district')
    list_filter = ('contact_name', 'district')

@admin.register(SupplierPayment)
class SupplierPaymentAdmin(admin.ModelAdmin):
    list_display = (
        'payment_date',
        'supplier',
        'amount',
    )
    list_filter = ('payment_date', 'supplier')
    search_fields = ('supplier__name',)