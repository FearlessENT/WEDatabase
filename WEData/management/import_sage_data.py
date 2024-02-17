import csv
from django.core.management.base import BaseCommand
from .models import Customer, Order, Part, PartDescription, Upholstery
from django.utils.dateparse import parse_date

class Command(BaseCommand):
    help = 'Imports data from SageOutputtedData.csv into the database'

    def handle(self, *args, **options):
        with open('/mnt/data/SageOutputtedData.csv', mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # Here you would create or update your model instances based on the row data
                # This is a simplified example; you'll need to adapt it to your specific data structure
                customer, _ = Customer.objects.get_or_create(name=row['CustomerName'])
                order, _ = Order.objects.get_or_create(
                    sage_order_number=row['SageOrderNumber'],
                    customer=customer,
                    order_date=parse_date(row['OrderDate']),
                    # Include other fields as necessary
                )
                # Continue for other models like Part, Upholstery, etc.

                # Handle foreign key relationships, e.g., creating Parts and linking to the Order
                part_description, _ = PartDescription.objects.get_or_create(
                    product_code=row['ProductCode'],
                    defaults={'product_description': row['ProductDescription']}
                )
                part, _ = Part.objects.get_or_create(
                    sage_order_number=order,
                    product_code=part_description,
                    # Include other fields as necessary
                )

                # Example for upholstery, assuming it's linked to a part
                upholstery, _ = Upholstery.objects.get_or_create(
                    part=part,
                    comments=row.get('Comments'),
                    # Handle other fields and conversions as needed
                )

                print(f'Imported {order.sage_order_number} and related data.')

        self.stdout.write(self.style.SUCCESS('Successfully imported data from SageOutputtedData.csv'))
