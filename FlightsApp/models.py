from mongoengine import Document, StringField, DateField, IntField

# Modèle pour les vols
class Flight(Document):
    destination = StringField(required=True, max_length=100)
    departure_date = DateField(required=True)
    price = IntField(required=True)
    seats_available = IntField(required=True)
    duration = IntField(required=True)

    def __str__(self):
        return f"{self.destination} - {self.departure_date}"

    # Modèle pour les réservations
class Reservation(Document):
        user_id = StringField(required=True)
        flight = StringField(required=True)
        reservation_date = DateField()

        def __str__(self):
            return f"Reservation for {self.flight.destination}"