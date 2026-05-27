from .models import CarMake, CarModel


def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars from Japan"},
        {"name": "Mercedes", "description": "Great cars from Germany"},
        {"name": "Audi", "description": "Great cars from Germany"},
        {"name": "Kia", "description": "Great cars from Korea"},
        {"name": "Toyota", "description": "Great cars from Japan"},
        {"name": "Honda", "description": "Reliable cars from Japan"},
        {"name": "Ford", "description": "American classic automaker"},
        {"name": "Chevrolet", "description": "American cars since 1911"},
    ]

    car_make_instances = []
    for data in car_make_data:
        make, _ = CarMake.objects.get_or_create(name=data["name"], defaults={"description": data["description"]})
        car_make_instances.append(make)

    car_model_data = [
        {"name": "Pathfinder", "car_type": "SUV", "year": 2023, "car_make": "NISSAN"},
        {"name": "Qashqai", "car_type": "SUV", "year": 2022, "car_make": "NISSAN"},
        {"name": "XTRAIL", "car_type": "SUV", "year": 2021, "car_make": "NISSAN"},
        {"name": "A-Class", "car_type": "SUV", "year": 2023, "car_make": "Mercedes"},
        {"name": "C-Class", "car_type": "Sedan", "year": 2023, "car_make": "Mercedes"},
        {"name": "E-Class", "car_type": "Sedan", "year": 2023, "car_make": "Mercedes"},
        {"name": "A4", "car_type": "Sedan", "year": 2023, "car_make": "Audi"},
        {"name": "A5", "car_type": "Coupe", "year": 2022, "car_make": "Audi"},
        {"name": "A6", "car_type": "Sedan", "year": 2023, "car_make": "Audi"},
        {"name": "Sorento", "car_type": "SUV", "year": 2023, "car_make": "Kia"},
        {"name": "Carnival", "car_type": "SUV", "year": 2023, "car_make": "Kia"},
        {"name": "Cerato", "car_type": "Sedan", "year": 2023, "car_make": "Kia"},
        {"name": "Corolla", "car_type": "Sedan", "year": 2023, "car_make": "Toyota"},
        {"name": "Camry", "car_type": "Sedan", "year": 2023, "car_make": "Toyota"},
        {"name": "RAV4", "car_type": "SUV", "year": 2023, "car_make": "Toyota"},
        {"name": "Civic", "car_type": "Sedan", "year": 2023, "car_make": "Honda"},
        {"name": "Accord", "car_type": "Sedan", "year": 2023, "car_make": "Honda"},
        {"name": "CR-V", "car_type": "SUV", "year": 2023, "car_make": "Honda"},
        {"name": "Mustang", "car_type": "Coupe", "year": 2023, "car_make": "Ford"},
        {"name": "Explorer", "car_type": "SUV", "year": 2023, "car_make": "Ford"},
        {"name": "F-150", "car_type": "Truck", "year": 2023, "car_make": "Ford"},
        {"name": "Malibu", "car_type": "Sedan", "year": 2023, "car_make": "Chevrolet"},
        {"name": "Tahoe", "car_type": "SUV", "year": 2023, "car_make": "Chevrolet"},
        {"name": "Silverado", "car_type": "Truck", "year": 2023, "car_make": "Chevrolet"},
    ]

    for data in car_model_data:
        make = CarMake.objects.get(name=data["car_make"])
        CarModel.objects.get_or_create(
            name=data["name"],
            car_make=make,
            defaults={"car_type": data["car_type"], "year": data["year"]}
        )
