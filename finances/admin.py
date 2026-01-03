from django.contrib import admin

# Register your models here.
from .models import ExpenseType, Expense

# Register your models here.
@admin.register(ExpenseType)
class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'is_active',
        'created_at',
        'updated_at'
    )
    search_fields = ('name', 'description')
    list_filter = ('is_active',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'expense_date',
        'expense_type',
        'amount',
        'description',
        'created_at',
        'updated_at'
    )
    search_fields = ('expense_date', 'expense_type', 'description')
    list_filter = ('expense_date', 'expense_type', 'amount')