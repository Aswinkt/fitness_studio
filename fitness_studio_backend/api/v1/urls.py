from django.urls import path
from .views import FitnessClassViewSet, BookingViewSet

urlpatterns = [
    path('classes/', FitnessClassViewSet.as_view({'get': 'list'}), name='class-list'),
    path('book/', BookingViewSet.as_view({'post': 'create'}), name='book-create'),
    path('bookings/', BookingViewSet.as_view({'get': 'my_bookings'}), name='my-bookings'),
]
