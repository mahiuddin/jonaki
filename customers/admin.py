from django.contrib import admin

# Register your models here.
from .models import CustomerType, Customer

@admin.register(CustomerType)
class CustomerTypeAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'created_at', 'updated_at')
    search_fields = ('name',)
    

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'customer_type',
        'district',
        'area',
        'created_at'
    )
    search_fields = ('name', 'phone', 'contact_person')
    list_filter = ('customer_type', 'district')