import csv
from django.core.management.base import BaseCommand
from products.models import Product, ProductCategory, ProductType, Brand


class Command(BaseCommand):
    help = 'Import products from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, skipinitialspace=True)

            for row in reader:
                row = {k.strip(): v for k, v in row.items()}

                # -------------------------
                # Resolve Product Type
                # -------------------------
                product_type_name = row.get('size_type')
                product_type_id = None

                if product_type_name:
                    try:
                        product_type_id = ProductType.objects.get(
                            name__iexact=product_type_name.strip()
                        ).id
                    except ProductType.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(
                                f"ProductType '{product_type_name}' not found"
                            )
                        )
                        continue

                # -------------------------
                # Resolve Category
                # -------------------------
                try:
                    category_id = ProductCategory.objects.get(
                        id=row['category_id']
                    ).id
                except ProductCategory.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Category ID '{row['category_id']}' not found"
                        )
                    )
                    continue

                # -------------------------
                # Resolve Brand
                # -------------------------
                brand_id = None
                if row.get('brand_id'):
                    try:
                        brand_id = Brand.objects.get(
                            id=row['brand_id']
                        ).id
                    except Brand.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Brand ID '{row['brand_id']}' not found"
                            )
                        )
                        continue

                # -------------------------
                # Convert numeric values
                # -------------------------
                quantity = float(row['quantity']) if row.get('quantity') else 0
                buying_price = float(row['buying_price'])
                discount_price = (
                    float(row['discount_price'])
                    if row.get('discount_price') else None
                )

                # -------------------------
                # Create or Update Product
                # -------------------------
                Product.objects.update_or_create(
                    sku=row['sku'],   # SKU is unique
                    defaults={
                        'name': row['name'],
                        'category_id': category_id,
                        'product_type_id': product_type_id,
                        'brand_id': brand_id,
                        'measurement_type': row['measurement_type'],
                        'size': row.get('size'),
                        'quantity': quantity,
                        'buying_price': buying_price,
                        'discount_price': discount_price,
                        'description': row.get('description'),
                        'status': row.get('status'),
                    }
                )

        self.stdout.write(
            self.style.SUCCESS("Products imported successfully")
        )
