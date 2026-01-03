import csv
from django.core.management.base import BaseCommand
from orders.models import Order
from customers.models import Customer


class Command(BaseCommand):
    help = 'Import orders from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, skipinitialspace=True)

            for row in reader:
                row = {k.strip(): v for k, v in row.items()}

                # -------------------------
                # Resolve Customer
                # -------------------------
                Customer_name = row.get('customer_name')
                customer_id = None

                if Customer_name:
                    try:
                        customer_id = Customer.objects.get(
                            name__iexact=Customer_name.strip()
                        ).id
                    except Customer.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Customer '{Customer_name}' not found"
                            )
                        )
                        continue


                # -------------------------
                # Convert numeric values
                # -------------------------
                gross_amount = float(row['gross_amount']) if row.get('gross_amount') else 0
                sale_amount = float(row['sale_amount']) if row.get('sale_amount') else 0
                profit = float(row['profit']) if row.get('profit') else 0
                discount = (
                    float(row['discount'])
                    if row.get('discount') else None
                )

                # -------------------------
                # Create or Update Order                
                # -------------------------
                Order.objects.update_or_create(
                    memo_number=row['memo_number'],   # Memo number is unique
                    defaults={
                        'order_date': row['order_date'],
                        'order_time': row['order_time'],
                        'customer_id': customer_id,
                        'gross_amount': gross_amount,
                        'sale_amount': sale_amount,
                        'profit': profit,
                        'discount': discount,
                        'status': row.get('status'),
                    }
                )

        self.stdout.write(
            self.style.SUCCESS("Orders imported successfully")
        )
