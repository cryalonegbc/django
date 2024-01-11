from django.core.management.base import BaseCommand
from ...models import Car

class Command(BaseCommand):
    help = 'Show information about all cars'

    def handle(self, *args, **options):
        cars = Car.objects.all()

        if cars:
            self.stdout.write(self.style.SUCCESS('List of cars:'))
            for car in cars:
                self.stdout.write(self.style.SUCCESS(f"{car.brand} {car.model} ({car.year}) - {car.price}руб."))
                self.stdout.write(self.style.SUCCESS(f"Description: {car.description}"))
                self.stdout.write("\n")
        else:
            self.stdout.write(self.style.WARNING('No cars found.'))
