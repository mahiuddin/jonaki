import csv
from django.http import HttpResponse
from django.contrib import admin, messages

from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.db import transaction
from .forms import ProductPriceImportForm

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
    list_filter = ('brand', 'product_type', 'status')
    search_fields = ('name', 'sku')
    
    
    def export_product_prices(modeladmin, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=product_prices.csv'

        writer = csv.writer(response)
        writer.writerow(['sku', 'name', 'buying_price', 'discount_price'])

        for product in queryset:
            writer.writerow([
                product.sku,
                product.name,
                product.buying_price,
                product.discount_price
            ])

        return response    


    def import_product_prices(self, request):
        if request.method == "POST":
            form = ProductPriceImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data['csv_file']

                decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
                reader = csv.DictReader(decoded_file)

                updated = 0
                skipped = 0

                with transaction.atomic():
                    for row in reader:
                        sku = row['sku'].strip()

                        try:
                            product = Product.objects.get(sku=sku)
                            product.buying_price = row['buying_price']
                            product.discount_price = row.get('discount_price') or 0
                            product.save()
                            updated += 1
                        except Product.DoesNotExist:
                            skipped += 1

                messages.success(
                    request,
                    f"Updated: {updated}, Skipped: {skipped}"
                )
                return redirect("..")
        else:
            form = ProductPriceImportForm()

        context = {
            "form": form,
            "title": "Import Product Prices"
        }
        return render(request, "admin/import_product_prices.html", context)

    # change_list_template = "admin/products/product/change_list.html"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import-prices/',
                self.admin_site.admin_view(self.import_product_prices),
                name='import-product-prices',
            ),
        ]
        return custom_urls + urls
    
    def import_prices_button(self):
        url = reverse('admin:import-product-prices')
        return format_html(
            '<a class="button" href="{}">⬆ Import Product Prices</a>',
            url
        )

    import_prices_button.short_description = ""


    actions = [export_product_prices]