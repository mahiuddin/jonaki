from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=12, decimal_places=2)
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

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.name} - {self.salary_date} - {self.amount}"
    
