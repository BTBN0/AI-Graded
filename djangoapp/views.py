from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CarMake, CarModel
from .populate import initiate


# Static dealer data (simulating external Cloudant DB)
DEALERS = [
    {"id": 1, "full_name": "Salena Motors", "city": "Wichita", "address": "123 Main St", "zip": "67201", "lat": 37.6872, "long": -97.3301, "short_name": "salena_motors", "st": "KS", "state": "Kansas"},
    {"id": 2, "full_name": "Sunshine Cars", "city": "Topeka", "address": "456 Oak Ave", "zip": "66601", "lat": 39.0558, "long": -95.6894, "short_name": "sunshine_cars", "st": "KS", "state": "Kansas"},
    {"id": 3, "full_name": "Prairie Auto Group", "city": "Kansas City", "address": "789 Elm Blvd", "zip": "66101", "lat": 39.0997, "long": -94.5786, "short_name": "prairie_auto", "st": "KS", "state": "Kansas"},
    {"id": 4, "full_name": "Golden State Motors", "city": "Los Angeles", "address": "100 Sunset Blvd", "zip": "90001", "lat": 34.0522, "long": -118.2437, "short_name": "golden_state", "st": "CA", "state": "California"},
    {"id": 5, "full_name": "Bay Area Cars", "city": "San Francisco", "address": "200 Market St", "zip": "94101", "lat": 37.7749, "long": -122.4194, "short_name": "bay_area_cars", "st": "CA", "state": "California"},
    {"id": 6, "full_name": "Lone Star Dealership", "city": "Houston", "address": "300 Texas Ave", "zip": "77001", "lat": 29.7604, "long": -95.3698, "short_name": "lone_star", "st": "TX", "state": "Texas"},
    {"id": 7, "full_name": "Empire Auto Sales", "city": "New York", "address": "400 Broadway", "zip": "10001", "lat": 40.7128, "long": -74.0060, "short_name": "empire_auto", "st": "NY", "state": "New York"},
    {"id": 8, "full_name": "Great Lakes Motors", "city": "Chicago", "address": "500 Lake Shore Dr", "zip": "60601", "lat": 41.8781, "long": -87.6298, "short_name": "great_lakes", "st": "IL", "state": "Illinois"},
]

REVIEWS = [
    {"id": 1, "dealer_id": 1, "reviewer": "Alice", "review": "Great service!", "sentiment": "positive", "purchase": True, "car_make": "Toyota", "car_model": "Camry", "car_year": 2022},
    {"id": 2, "dealer_id": 1, "reviewer": "Bob", "review": "Very helpful staff.", "sentiment": "positive", "purchase": False, "car_make": "Honda", "car_model": "Civic", "car_year": 2021},
    {"id": 3, "dealer_id": 2, "reviewer": "Carol", "review": "Average experience.", "sentiment": "neutral", "purchase": True, "car_make": "Ford", "car_model": "Explorer", "car_year": 2023},
    {"id": 4, "dealer_id": 3, "reviewer": "Dave", "review": "Fantastic services", "sentiment": "positive", "purchase": True, "car_make": "Chevrolet", "car_model": "Malibu", "car_year": 2022},
]


def get_dealerships(request, state="All"):
    if state == "All":
        dealers = DEALERS
    else:
        dealers = [d for d in DEALERS if d["state"].lower() == state.lower() or d["st"].lower() == state.lower()]
    return JsonResponse({"status": 200, "dealers": dealers})


def get_dealer_details(request, dealer_id):
    dealers = [d for d in DEALERS if d["id"] == dealer_id]
    if dealers:
        return JsonResponse({"status": 200, "dealer": dealers[0]})
    return JsonResponse({"status": 404, "message": "Dealer not found"}, status=404)


def get_dealer_reviews(request, dealer_id):
    reviews = [r for r in REVIEWS if r["dealer_id"] == dealer_id]
    return JsonResponse({"status": 200, "reviews": reviews})


def get_cars(request):
    if not CarMake.objects.exists():
        initiate()
    car_makes = CarMake.objects.prefetch_related('carmodel_set').all()
    result = []
    for make in car_makes:
        models_list = [{"name": m.name, "type": m.car_type, "year": m.year} for m in make.carmodel_set.all()]
        result.append({"make": make.name, "models": models_list})
    return JsonResponse({"CarMakes": result})


def analyze_review_sentiment(request):
    text = request.GET.get("text", "")
    if not text:
        return JsonResponse({"sentiment": "unknown"})

    text_lower = text.lower()
    positive_words = ["great", "excellent", "fantastic", "amazing", "wonderful", "good", "best", "love", "perfect", "outstanding"]
    negative_words = ["bad", "terrible", "awful", "horrible", "worst", "hate", "poor", "disappointing", "negative"]

    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)

    if pos_count > neg_count:
        sentiment = "positive"
    elif neg_count > pos_count:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return JsonResponse({"sentiment": sentiment, "text": text})


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        return JsonResponse({"userName": username, "status": "Failed"})
    return JsonResponse({"error": "POST required"}, status=405)


def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")
        first_name = data.get("firstName", "")
        last_name = data.get("lastName", "")
        email = data.get("email", "")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"userName": username, "error": "Already Registered"})

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    return JsonResponse({"error": "POST required"}, status=405)


@csrf_exempt
def add_review(request):
    if request.method == "POST":
        data = json.loads(request.body)
        REVIEWS.append({
            "id": len(REVIEWS) + 1,
            "dealer_id": data.get("dealerId"),
            "reviewer": data.get("reviewer", "Anonymous"),
            "review": data.get("review", ""),
            "sentiment": "positive",
            "purchase": data.get("purchase", False),
            "car_make": data.get("carMake", ""),
            "car_model": data.get("carModel", ""),
            "car_year": data.get("carYear", 2023),
        })
        return JsonResponse({"status": 200})
    return JsonResponse({"error": "POST required"}, status=405)
