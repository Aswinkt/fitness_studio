from rest_framework import serializers
from bookings.models import FitnessClass, Booking


class FitnessClassSerializer(serializers.ModelSerializer):
    """
    Serializer for FitnessClass model.
    """

    class_type_display = serializers.CharField(
        source="get_class_type_display", read_only=True
    )
    formatted_start_time = serializers.SerializerMethodField()
    formatted_end_time = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = [
            "id",
            "name",
            "class_type",
            "class_type_display",
            "description",
            "instructor",
            "start_time",
            "end_time",
            "formatted_start_time",
            "formatted_end_time",
            "total_slots",
            "available_slots",
        ]

    def get_formatted_start_time(self, obj):
        """Format start time as 'DD MMM YYYY HH:MM AM/PM'."""
        return obj.start_time.strftime("%d %b %Y %I:%M %p")

    def get_formatted_end_time(self, obj):
        """Format end time as 'DD MMM YYYY HH:MM AM/PM'."""
        return obj.end_time.strftime("%d %b %Y %I:%M %p")


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model.
    """

    class_name = serializers.CharField(
        source="fitness_class.get_class_type_display", read_only=True
    )
    formatted_booking_date = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            "id",
            "fitness_class",
            "class_name",
            "client_name",
            "client_email",
            "booking_date",
            "formatted_booking_date",
            "is_cancelled",
        ]
        read_only_fields = ["booking_date", "is_cancelled"]

    def get_formatted_booking_date(self, obj):
        """Format booking date as 'DD MMM YYYY HH:MM AM/PM'."""
        return obj.booking_date.strftime("%d %b %Y %I:%M %p")


class BookingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new bookings.
    """

    class Meta:
        model = Booking
        fields = ["fitness_class", "client_name", "client_email"]
