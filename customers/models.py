from datetime import timezone
from django.db import models
from common.constants import CONTACT_TYPE_CHOICES, DISTRICT_CHOICES, NO_SALE_REASON_CHOICES, RESPONSE_TYPE_CHOICES

# Create your models here.
class CustomerType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Customer Type"
        verbose_name_plural = "Customer Types"

    def __str__(self):
        return self.name

    
class Customer(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=100, blank=True, null=True)
    customer_type = models.ForeignKey(
        CustomerType,
        on_delete=models.PROTECT,
        related_name='customers'
    )
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    contact_person_number = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(
       max_length=100,
       choices=DISTRICT_CHOICES
    )
    area = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
    
    def __str__(self):
        return self.name

class NoSaleReason(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='no_sale_visits'
    )

    reason = models.CharField(
        max_length=30,
        choices=NO_SALE_REASON_CHOICES
    )
    visiting_date = models.DateField()

    visiting_time = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.name} - {self.get_reason_display()} - {self.visiting_date}"
    

class CustomerFollowUp(models.Model):

    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        related_name='contacts'
    )
    contact_date = models.DateField()
    contact_time = models.TimeField(
        blank=True,
        null=True
    )

    contact_type = models.CharField(
        max_length=10,
        choices=CONTACT_TYPE_CHOICES,
        default='phone'
    )

    response_type = models.CharField(
        max_length=20,
        choices=RESPONSE_TYPE_CHOICES
    )

    next_contact_date = models.DateField(
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer} - {self.contact_date} ({self.contact_type})"
