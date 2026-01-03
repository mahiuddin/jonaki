import csv
from django.core.management.base import BaseCommand
from finances.models import ExpenseType, Expense

class Command(BaseCommand):
    help = 'Import expenses from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, skipinitialspace=True)

            for row in reader:
                # 🔍 DEBUG (keep this for now)
                print(row)

                expense_date = row['expense_date'].strip()
                expense_type_name = row['expense_type'].strip()
                amount = row['amount'].strip()
                description = row.get('description')

                # Get or create the ExpenseType
                expense_type, created = ExpenseType.objects.get_or_create(
                    name=expense_type_name
                )

                Expense.objects.create(
                    expense_date=expense_date,
                    expense_type=expense_type,
                    amount=amount,
                    description=description
                )

        self.stdout.write(self.style.SUCCESS("Expenses imported successfully"))