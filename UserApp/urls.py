from django.urls import path
from . import views  # Assuming your views are in views.py in the same app

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

    # Frontoffice
    #path('flights/', views.available_flights, name='available_flights'),
    path('reserve/<str:flight_id>/', views.reserve_flight, name='reserve_flight'),
    path('reservations/', views.my_reservations, name='my_reservations'),
    path('cancel-reservation/<str:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),

]