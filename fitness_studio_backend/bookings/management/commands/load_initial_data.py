from django.core.management.base import BaseCommand
import random
from datetime import datetime, timedelta
import pytz
from bookings.models import FitnessClass, Booking


class Command(BaseCommand):
    help = "Loads initial sample data for the fitness studio"

    def handle(self, *args, **kwargs):
        """Create sample fitness classes and bookings."""
        # Clear existing data
        FitnessClass.objects.all().delete()
        Booking.objects.all().delete()

        # Sample data
        instructors = [
            "Emma Thompson",
            "Michael Chen",
            "Priya Sharma",
            "David Wilson",
            "Sophie Anderson",
        ]

        class_names = {
            "YOGA": [
                "Morning Yoga Flow",
                "Power Yoga Session",
                "Yin Yoga Practice",
                "Vinyasa Flow",
                "Meditation & Yoga"
            ],
            "ZUMBA": [
                "Latin Dance Party",
                "Zumba Fitness",
                "Dance Cardio",
                "Zumba Toning",
                "Aqua Zumba"
            ],
            "HIIT": [
                "High Intensity Training",
                "Tabata Workout",
                "Circuit Training",
                "Strength & Cardio",
                "Full Body HIIT"
            ]
        }

        class_descriptions = {
            "YOGA": [
                "A gentle morning yoga session to start your day with energy and mindfulness.",
                "An intense power yoga session focusing on strength and flexibility.",
                "A calming yin yoga practice for deep stretching and relaxation.",
                "A dynamic vinyasa flow class connecting breath with movement.",
                "A peaceful meditation and yoga session for mental clarity."
            ],
            "ZUMBA": [
                "An energetic Latin dance party that burns calories while having fun.",
                "A high-energy Zumba class combining dance and fitness.",
                "A cardio-focused dance workout to upbeat music.",
                "A Zumba class incorporating light weights for toning.",
                "A refreshing pool-based Zumba workout."
            ],
            "HIIT": [
                "A challenging high-intensity interval training session.",
                "A fast-paced Tabata workout with 20/10 intervals.",
                "A full-body circuit training session.",
                "A combination of strength training and cardio exercises.",
                "An intense full-body HIIT workout for maximum calorie burn."
            ]
        }

        # Create fitness classes
        ist = pytz.timezone("Asia/Kolkata")
        base_date = datetime.now(ist).replace(hour=8, minute=0, second=0, microsecond=0)

        classes = []
        for i in range(15):  # Create 15 classes
            class_type = random.choice(["YOGA", "ZUMBA", "HIIT"])
            start_time = base_date + timedelta(days=i // 3, hours=i % 3 * 2)
            end_time = start_time + timedelta(hours=1)
            
            # Get matching name and description
            name_index = random.randint(0, len(class_names[class_type]) - 1)
            name = class_names[class_type][name_index]
            description = class_descriptions[class_type][name_index]

            fitness_class = FitnessClass.objects.create(
                name=name,
                class_type=class_type,
                description=description,
                instructor=random.choice(instructors),
                start_time=start_time,
                end_time=end_time,
                total_slots=random.randint(10, 20),
                available_slots=random.randint(5, 20),
            )
            classes.append(fitness_class)

        # Create bookings
        clients = [
            ("Sarah Smith", "sarah@example.com"),
            ("John Doe", "john@example.com"),
            ("Maria Garcia", "maria@example.com"),
            ("Raj Patel", "raj@example.com"),
            ("Emma Wilson", "emma@example.com"),
            ("David Kim", "david@example.com"),
            ("Lisa Chen", "lisa@example.com"),
            ("Alex Brown", "alex@example.com"),
        ]

        # Track which classes each client has booked
        client_bookings = {email: set() for _, email in clients}
        bookings_created = 0
        max_attempts = 100  # Prevent infinite loop

        while bookings_created < 20 and max_attempts > 0:
            fitness_class = random.choice(classes)
            client_name, client_email = random.choice(clients)

            # Skip if client already booked this class
            if fitness_class.id in client_bookings[client_email]:
                max_attempts -= 1
                continue

            # Only create booking if there are available slots
            if fitness_class.available_slots > 0:
                Booking.objects.create(
                    fitness_class=fitness_class,
                    client_name=client_name,
                    client_email=client_email,
                )
                fitness_class.available_slots -= 1
                fitness_class.save()
                client_bookings[client_email].add(fitness_class.id)
                bookings_created += 1
            max_attempts -= 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {FitnessClass.objects.count()} classes and "
                f"{Booking.objects.count()} bookings"
            )
        )
