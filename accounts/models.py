from time import timezone
from django.db import models

from common.constants import FIXED_HOLIDAY_CHOICES, LEAVE_REASON_CHOICES

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    salary = models.IntegerField(help_text="Employee's monthly salary")
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # correct: function, no ()
    updated_at = models.DateTimeField(auto_now=True)  # will set initial value

    def __str__(self):
        return self.name

class Salary(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='salaries'
    )

    salary_date = models.DateField()

    amount = models.IntegerField(
        help_text="Salary amount"
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'salary_date'],
                name='unique_employee_salary_date'
            )
        ]

    def __str__(self):
        return f"{self.employee.name} - {self.salary_date} - {self.amount}"
    
class Attendance(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendances'
    )

    attendance_date = models.DateField()

    in_time = models.TimeField()
    out_time = models.TimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'attendance_date'],
                name='unique_employee_attendance_date'
            )
        ]

    def __str__(self):
        return f"{self.employee.name} - {self.attendance_date}"
    
class Leave(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='leaves'
    )

    leave_date = models.DateField()

    leave_reason = models.CharField(
        max_length=20,
        choices=LEAVE_REASON_CHOICES
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'leave_date'],
                name='unique_employee_leave_date'
            )
        ]

    def __str__(self):
        return f"{self.employee.name} - {self.get_leave_reason_display()} ({self.leave_date})"
    
class Holiday(models.Model):
    holiday_date = models.DateField(
        unique=True,
        help_text="Official holiday date"
    )

    name = models.CharField(
        max_length=250,
        choices=FIXED_HOLIDAY_CHOICES,
        help_text="Fixed day of the year for holiday"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.holiday_date}"