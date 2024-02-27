#!/bin/bash





# Function to wait for MySQL
wait_for_db() {
    echo "waiting for database"

    sleep 15

    echo "database ready"
}

# Wait for the MySQL database to be ready
wait_for_db





# Apply database migrations
echo "Applying database migrations..."
# python manage.py makemigrations
# python manage.py migrate 
python manage.py collectstatic  --no-input




# Create a superuser if SUPERUSER_CREATE is set to true
# and if the superuser does not already exist
if [ "$SUPERUSER_CREATE" = "true" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --no-input
fi











# Start the Django app
echo "Starting Django app..."
# exec "$@"
