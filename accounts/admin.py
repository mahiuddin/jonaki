from django.contrib import admin
from .models import Employee, Salary
# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name','salary','phone', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'salary_date', 'amount')
    list_filter = ('salary_date', 'employee')
    search_fields = ('employee__name',)