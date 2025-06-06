from django.contrib import admin
from .models import FitnessClass, Booking

@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ('get_class_type_display', 'instructor', 'start_time', 'available_slots')
    list_filter = ('class_type', 'instructor')
    search_fields = ('class_type', 'instructor', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'fitness_class', 'booking_date', 'is_cancelled')
    list_filter = ('is_cancelled', 'booking_date')
    search_fields = ('client_name', 'client_email')
