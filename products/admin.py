from django.contrib import admin

# Register your models here.
from .models import Brand, Product, ProductCategory, ProductType

# admin.site.register(Brand)
# admin.site.register(ProductCategory)
# admin.site.register(ProductType)
# admin.site.register(Employee)

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','short_code', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_code', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name','country', 'short_code', 'description','is_active', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'sku', 'category', 'brand',
        'quantity', 'buying_price', 'status'
    )
    list_filter = ('category', 'brand', 'status')
    search_fields = ('name', 'sku')