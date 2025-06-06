# Fitness Studio Booking API

A Django REST Framework API for managing fitness class bookings.

## Features

- View available fitness classes
- Book classes with client information
- View personal bookings
- Automatic timezone handling (IST)
- Input validation and error handling

## API Endpoints

### Classes

- `GET /api/v1/classes/` - List all available classes
- `GET /api/v1/classes/{id}/` - Get details of a specific class

### Bookings

- `POST /api/v1/bookings/` - Create a new booking
- `GET /api/v1/bookings/my-bookings/?email=client@example.com` - View personal bookings

## Example Usage

### Creating a Booking

```bash
curl -X POST http://localhost:8000/api/v1/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "fitness_class": 1,
    "client_name": "Sarah Smith",
    "client_email": "sarah@example.com"
  }'
```

### Viewing Personal Bookings

```bash
curl http://localhost:8000/api/v1/bookings/my-bookings/?email=sarah@example.com
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Start the server:
   ```bash
   python manage.py runserver
   ```

## Available Class Types

- Yoga
- Zumba
- HIIT

## Timezone

All times are handled in Indian Standard Time (IST).