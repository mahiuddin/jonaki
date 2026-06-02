from django.contrib import admin
from django.db import models
from django.forms import TimeInput
from .models import Attendance, Employee, EmployeeOutsideLog, Holiday, Leave, Salary
# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name','salary','phone', 'meal_allowance', 'snacks_allowance', 'hourly_rate', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'salary_date', 'amount')
    list_filter = ('salary_date', 'employee')
    search_fields = ('employee__name',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TimeField: {
            'widget': TimeInput(
                attrs={
                    'type': 'time'
                }
            )
        }
    }
    list_display = ('employee', 'attendance_date', 'in_time', 'out_time', 'remarks')
    list_filter = ('attendance_date',)
    date_hierarchy = 'attendance_date'
    search_fields = ('employee__name',)

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_date', 'leave_reason', 'description')
    list_filter = ('leave_reason', 'leave_date')
    date_hierarchy = 'leave_date'
    search_fields = ('employee__name',)

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('holiday_date', 'name')
    date_hierarchy = 'holiday_date'
    search_fields = ('name',)

@admin.register(EmployeeOutsideLog)
class EmployeeOutsideLogAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TimeField: {
            'widget': TimeInput(
                attrs={
                    'type': 'time'
                }
            )
        }
    }
    list_display = ('employee', 'outing_date', 'out_time', 'in_time','duration_minutes','reason')
    list_filter = ('outing_date', 'employee','reason')
    date_hierarchy = 'outing_date'
    search_fields = ('employee__name', 'reason')  