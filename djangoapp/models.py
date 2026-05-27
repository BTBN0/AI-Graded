from django.db import models


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    COUPE = 'Coupe'
    TRUCK = 'Truck'
    VAN = 'Van'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (COUPE, 'Coupe'),
        (TRUCK, 'Truck'),
        (VAN, 'Van'),
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=10, choices=CAR_TYPES, default=SEDAN)
    year = models.IntegerField(default=2023)
    dealer_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
