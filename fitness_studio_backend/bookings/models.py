from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
import pytz

class FitnessClass(models.Model):
    """
    Model representing a fitness class in the studio.
    
    Attributes:
        CLASS_TYPES: Choices for class types (YOGA, ZUMBA, HIIT)
        class_type: Type of fitness class
        description: Detailed description of the class
        instructor: Name of the class instructor
        start_time: When the class starts
        end_time: When the class ends
        total_slots: Total number of slots available
        available_slots: Number of slots still available
        created_at: When the class was created
        updated_at: When the class was last updated
    """
    CLASS_TYPES = [
        ('YOGA', 'Yoga'),
        ('ZUMBA', 'Zumba'),
        ('HIIT', 'HIIT'),
    ]

    name = models.CharField(max_length=100)
    class_type = models.CharField(max_length=10, choices=CLASS_TYPES)
    description = models.TextField(blank=True, help_text="Brief description of the class")
    instructor = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_slots = models.IntegerField(validators=[MinValueValidator(1)])
    available_slots = models.IntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} with {self.instructor} at {self.start_time}"

    def save(self, *args, **kwargs):
        """
        Override save method to ensure times are in IST timezone.
        Converts naive datetime objects to timezone-aware ones in IST.
        """
        ist = pytz.timezone('Asia/Kolkata')
        if self.start_time.tzinfo is None:
            self.start_time = timezone.make_aware(self.start_time, timezone=ist)
        if self.end_time.tzinfo is None:
            self.end_time = timezone.make_aware(self.end_time, timezone=ist)
        super().save(*args, **kwargs)

class Booking(models.Model):
    """
    Model representing a booking for a fitness class.
    
    Attributes:
        fitness_class: The class being booked (ForeignKey to FitnessClass)
        client_name: Name of the person booking
        client_email: Email of the person booking
        booking_date: When the booking was made
        is_cancelled: Whether the booking is cancelled
    
    Meta:
        unique_together: Ensures a client can only book a class once
    """
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='bookings')
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booking_date = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client_name}'s booking for {self.fitness_class.name}"

    class Meta:
        unique_together = ('fitness_class', 'client_email')
