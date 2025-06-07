from django.urls import path
from .views import FitnessClassViewSet, BookingViewSet

urlpatterns = [
    # GET /classes - List all upcoming fitness classes
    path('classes/', FitnessClassViewSet.as_view({'get': 'list'}), name='class-list'),
    
    # POST /book - Create a new booking
    path('book/', BookingViewSet.as_view({'post': 'create'}), name='book-create'),
    
    # GET /bookings - List bookings for a specific email
    path('bookings/', BookingViewSet.as_view({'get': 'my_bookings'}), name='my-bookings'),
]
