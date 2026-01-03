import csv
from django.core.management.base import BaseCommand
from accounts.models import Employee, Salary

class Command(BaseCommand):
    help = 'Import salaries from CSV file'
    def add_arguments(self, parser):        
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, skipinitialspace=True)

            for row in reader:
                # 🔍 DEBUG (keep this for now)
                print(row)

                salary_date = row['salary_date'].strip()
                amount = row['amount'].strip()
                description = row.get('description')

                Salary.objects.create(
                    salary_date=salary_date,
                    employee=Employee.objects.get(name=row['employee_name']),
                    amount=amount,
                    description=description
                )

        self.stdout.write(self.style.SUCCESS("Salaries imported successfully"))