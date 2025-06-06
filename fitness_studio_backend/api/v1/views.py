from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from bookings.models import FitnessClass, Booking
from .serializers import (
    FitnessClassSerializer, 
    BookingSerializer, 
    BookingCreateSerializer
)

class FitnessClassViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing fitness classes.
    
    Provides endpoints to:
    - List all upcoming fitness classes
    - Retrieve details of a specific class
    
    The list endpoint only returns classes that haven't started yet,
    ordered by their start time.
    """
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer

    def get_queryset(self):
        """
        Returns a queryset of upcoming fitness classes.
        
        Returns:
            QuerySet: Filtered queryset containing only future classes,
                     ordered by start time.
        """
        return FitnessClass.objects.filter(
            start_time__gt=timezone.now()
        ).order_by('start_time')

class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing class bookings.
    
    Provides endpoints to:
    - Create new bookings
    - List bookings for a specific email
    
    The create endpoint includes validation for:
    - Available slots
    - Duplicate bookings
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new booking for a fitness class.
        
        Args:
            request: The HTTP request containing booking details:
                    - fitness_class: ID of the class to book
                    - client_name: Name of the person booking
                    - client_email: Email of the person booking
        
        Returns:
            Response: 
                - 201 Created: If booking is successful
                - 400 Bad Request: If validation fails (no slots, duplicate booking)
        """
        serializer = BookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            fitness_class = FitnessClass.objects.get(id=request.data['fitness_class'])
            
            # Check if slots are available
            if fitness_class.available_slots <= 0:
                return Response(
                    {'error': 'No slots available for this class'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if user already has a booking for this class
            if Booking.objects.filter(
                fitness_class=fitness_class,
                client_email=request.data['client_email'],
                is_cancelled=False
            ).exists():
                return Response(
                    {'error': 'You already have a booking for this class'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create booking and update available slots
            booking = serializer.save()
            fitness_class.available_slots -= 1
            fitness_class.save()

            return Response(
                BookingSerializer(booking).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        """
        List all bookings for a specific email address.
        
        Args:
            request: The HTTP request containing:
                    - email: Query parameter with the email to search for
        
        Returns:
            Response:
                - 200 OK: List of bookings for the email
                - 400 Bad Request: If email parameter is missing
        """
        email = request.query_params.get('email')
        if not email:
            return Response(
                {'error': 'Email parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        bookings = Booking.objects.filter(
            client_email=email,
            is_cancelled=False
        ).order_by('-booking_date')
        
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
