import csv
from django.core.management.base import BaseCommand
from mobilebankings.models import MobileBankingProfit

class Command(BaseCommand):
    help = 'Import mobile banking profits from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, skipinitialspace=True)

            for row in reader:
                # 🔍 DEBUG (keep this for now)
                print(row)

                profit_date = row['Date'].strip()
                mobile_banking_category = row['Product'].strip()
                profit_amount = row['Profit'].strip()
            


                MobileBankingProfit.objects.create(
                    profit_date=profit_date,
                    mobile_banking_category=mobile_banking_category,
                    profit_amount=profit_amount
                )

        self.stdout.write(self.style.SUCCESS("Mobile banking profits imported successfully"))