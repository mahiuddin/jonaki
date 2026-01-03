import csv
from django.core.management.base import BaseCommand
from suppliers.models import Supplier

class Command(BaseCommand):
    help = 'Import suppliers from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, skipinitialspace=True)

            for row in reader:
                # 🔍 DEBUG (keep this for now)
                print(row)
                
                name = row['name'].strip()
                contact_name = row.get('contact_name')
                contact_number = row.get('contact_number')
                district = row.get('district')
                area = row.get('area')    
        
                if contact_number:
                    contact_number = str(contact_number).split('.')[0]

                Supplier.objects.create(
                    name=name,
                    contact_name=contact_name,
                    contact_number=contact_number,
                    district=district,
                    area=area
                )

        self.stdout.write(self.style.SUCCESS("Suppliers imported successfully"))