from django.shortcuts import render, redirect
from .models import Flight, Reservation
from django.contrib.auth.decorators import login_required
from datetime import date
# Create your views here.

# === Backoffice ===

# Liste des vols
def flight_list(request):
    flights = Flight.objects.all()
    return render(request, 'flight_list.html', {'flights': flights})

# Ajouter un vol
def add_flight(request):
    if request.method == 'POST':
        destination = request.POST['destination']
        departure_date = request.POST['departure_date']
        price = request.POST['price']
        seats_available = request.POST['seats_available']
        duration = request.POST['duration']  # Add duration field

        # Save the flight with the new 'duration' field
        Flight(destination=destination,
               departure_date=departure_date,
               price=price,
               seats_available=seats_available,
               duration=duration).save()
        return redirect('flight_list')
    return render(request, 'add_flight.html')

# Modifier un vol
def update_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    if request.method == 'POST':
        flight.destination = request.POST['destination']
        flight.departure_date = request.POST['departure_date']
        flight.price = request.POST['price']
        flight.seats_available = request.POST['seats_available']
        flight.duration = request.POST['duration']  # Update the duration field
        flight.save()
        return redirect('flight_list')
    return render(request, 'update_flight.html', {'flight': flight})

# Supprimer un vol
def delete_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    flight.delete()
    return redirect('flight_list')

# === Frontoffice ===

# Liste des vols disponibles
def available_flights(request):
    flights = Flight.objects.filter(seats_available__gt=0)
    return render(request, 'available_flights.html', {'flights': flights})

