from django.urls import path
from . import views

urlpatterns = [
    # Backoffice CRUD
    path('admin/flights/', views.flight_list, name='flight_list'),
    path('admin/flights/add/', views.add_flight, name='add_flight'),
    path('admin/flights/update/<str:flight_id>/', views.update_flight, name='update_flight'),
    path('admin/flights/delete/<str:flight_id>/', views.delete_flight, name='delete_flight'),


]
