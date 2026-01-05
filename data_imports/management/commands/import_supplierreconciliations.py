import csv
from django.core.management.base import BaseCommand
from stocks.models import SupplierReconciliation
from suppliers.models import SupplierPayment,Supplier   

class Command(BaseCommand):
    help = 'Import supplier reconciliations from CSV file'

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
                SupplierReconciliation.objects.create(
                    reconciliation_date=row['stock_date'],
                    supplier=Supplier.objects.get(name=row['supplier']),
                    balance_amount=row['amount'],
                )

        self.stdout.write(
            self.style.SUCCESS("Supplier reconciliations imported successfully")
        )
