import csv
from django.core.management.base import BaseCommand
from customers.models import Customer, CustomerType

class Command(BaseCommand):
    help = 'Import customers from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, skipinitialspace=True)

            for row in reader:
                # 🔍 DEBUG (keep this for now)
                print(row)

                customer_type_name = row['type'].strip()

                try:
                    customer_type = CustomerType.objects.get(
                        name__iexact=customer_type_name
                    )
                except CustomerType.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f"CustomerType '{customer_type_name}' not found"
                        )
                    )
                    continue

                phone = row['phone']
                if phone:
                    phone = str(phone).split('.')[0]

                Customer.objects.create(
                    name=row['name'],
                    phone=phone,
                    customer_type=customer_type,
                    contact_person=row.get('contact_person'),
                    contact_person_number=row.get('contact_person_phone'),
                    district=row['district'],
                    area=row['area']
                )

        self.stdout.write(self.style.SUCCESS("Customers imported successfully"))
