from django.db import models
from django.utils import timezone
from common.choices import COUNTRY_CHOICES,MEASUREMENT_UNIT_CHOICES,PRODUCT_STATUS_CHOICES

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES)
    short_code = models.TextField(blank=True, unique=True, default='nb')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_code = models.TextField(blank=True, unique=True, default='nc')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # set automatically when record is created
    updated_at = models.DateTimeField(auto_now=True)      # updated automatically on every save

    class Meta:
        ordering = ['name']  # optional, alphabetically in admin

    def __str__(self):
        return self.name
    
class ProductType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_code = models.TextField(blank=True, unique=True, default='npt')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']  # optional, alphabetically in admin
        verbose_name = "Product Type"
        verbose_name_plural = "Product Types"

    def __str__(self):
        return self.name
    
def save(self, *args, **kwargs):
    self.updated_at = timezone.now()
    super().save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=255)

    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name='products'
    )

    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.PROTECT,
        related_name='products',
        blank=True,
        null=True
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name='products',
        blank=True,
        null=True
    )

    sku = models.CharField(
        max_length=100,
        unique=True
    )

    measurement_type = models.CharField(
        max_length=20,
        choices=MEASUREMENT_UNIT_CHOICES
    )

    size = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    buying_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    discount_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=PRODUCT_STATUS_CHOICES,
        default='active'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deleted_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name