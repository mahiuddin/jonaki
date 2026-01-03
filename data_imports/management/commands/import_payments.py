import csv
from django.core.management.base import BaseCommand
from suppliers.models import SupplierPayment,Supplier   

class Command(BaseCommand):
    help = 'Import supplier payments  from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, skipinitialspace=True)

            for row in reader:
                row = {k.strip(): v for k, v in row.items()}


                # -------------------------
                # Create or Update Order                
                # -------------------------
                SupplierPayment.objects.create(
                    payment_date=row['payment_date'],   
                    supplier=Supplier.objects.get(name=row['name']),
                    amount=row['amount'],
                )

        self.stdout.write(
            self.style.SUCCESS("Supplier payments imported successfully")
        )
