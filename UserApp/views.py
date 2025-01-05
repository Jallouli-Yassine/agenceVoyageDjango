from django.http import Http404
from django.shortcuts import render, redirect
from mongoengine.errors import DoesNotExist
from FlightsApp.models import Flight
from FlightsApp.models import Reservation
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from datetime import date
from .models import User

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
        flights = flights.filter(seats_available__gte=int(num_people))

    # Get the logged-in user's reservations
    user_id = str("6779ffc2aeaaa328d63d5319")  # Replace with request.user.id for real authentication
    user_reservations = Reservation.objects.filter(user_id=user_id)

    # Extract the IDs of reserved flights as strings for comparison
    reserved_flight_ids = [str(reservation.flight) for reservation in user_reservations]

    # Debugging
    print(f"Reserved Flight IDs: {reserved_flight_ids}")
    print(f"user ID: {user_id}")
    print(f"Flight IDs in View: {[str(flight.id) for flight in flights]}")

    # Pass flights and reserved_flight_ids to the template
    return render(request, 'home.html', {
        'flights': flights,
        'reserved_flight_ids': reserved_flight_ids,
    })


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if user already exists
        if User.objects(email=email).first():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        # Save the user
        User(username=username, email=email,password=make_password(password)).save()
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Find the user by email
        user = User.objects(email=email).first()

        if user:
            # Verify the password
            if check_password(password, user.password):
                # Store user ID in session
                request.session['user_id'] = str(user.id)
                messages.success(request, 'Login successful.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid password.')
        else:
            messages.error(request, 'User does not exist.')

    return render(request, 'login.html')

# Réserver un vol
#@login_required


def reserve_flight(request, flight_id):
    try:
        # Retrieve the flight object from the database
        flight = Flight.objects.get(id=flight_id)
    except DoesNotExist:
        # If the flight doesn't exist, redirect to the available flights page
        return redirect('available_flights')

    # Check if there are available seats for the flight
    if flight.seats_available > 0:
        # Create the reservation, store the flight ID as a string
        Reservation(user_id=str("6779ffc2aeaaa328d63d5319"), flight=str(flight.id), reservation_date=date.today()).save()

        # Decrease the number of available seats by 1
        flight.seats_available -= 1
        flight.save()

        # Redirect to the user's reservations page
        return redirect('my_reservations')

    # If no seats are available, redirect back to the available flights page
    return redirect('available_flights')


def cancel_reservation(request, reservation_id):
    # Retrieve the reservation object
    reservation = Reservation.objects.get(id=reservation_id)


    # Increment the available seats for the flight
    flight = Flight.objects.get(id=reservation.flight)
    flight.seats_available += 1
    flight.save()

    # Delete the reservation
    reservation.delete()

    # Redirect to the 'my_reservations' page
    return redirect('my_reservations')

# Mes réservations
#@login_required

def my_reservations(request):
    # Get reservations for the current user (adjust user retrieval as needed)
    reservations = Reservation.objects.filter(user_id="6779ffc2aeaaa328d63d5319")

    # Fetch the flight details for each reservation
    reservation_details = []
    for reservation in reservations:
        try:
            flight = Flight.objects.get(id=reservation.flight)  # Fetch the full flight object
            reservation_details.append({
                "reservation": reservation,
                "flight": flight
            })
        except Flight.DoesNotExist:
            raise Http404(f"Flight with ID {reservation.flight} not found.")

    return render(request, 'my_reservations.html', {'reservation_details': reservation_details})