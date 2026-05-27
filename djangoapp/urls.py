from django.urls import path
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path('postreview/', views.post_review_page, name='post_review'),
    path('addedreview/', views.added_review_page, name='added_review'),
    path('', views.get_dealerships, name='index'),
    path('get_dealers/', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>/', views.get_dealerships, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    path('reviews/dealer/<int:dealer_id>/', views.get_dealer_reviews, name='dealer_reviews'),
    path('get_cars/', views.get_cars, name='get_cars'),
    path('analyze_review/', views.analyze_review_sentiment, name='analyze_review'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.registration, name='register'),
    path('add_review/', views.add_review, name='add_review'),
]
