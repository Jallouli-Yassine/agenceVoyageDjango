from django.shortcuts import render
from FlightsApp.models import Flight
from datetime import datetime, timedelta

def home(request):
    flights = Flight.objects.all()

    # Get form data from GET request
    destination = request.GET.get('destination')
    departure_date = request.GET.get('departure_date')
    num_people = request.GET.get('num_people')

    # Apply filters based on the form data
    if destination:
        flights = flights.filter(destination__icontains=destination)

    if departure_date:
        flights = flights.filter(departure_date__exact=departure_date)

    if num_people:
        # You can add logic to filter based on available seats
        flights = flights.filter(seats_available__gte=int(num_people))

    return render(request, 'home.html', {'flights': flights})
