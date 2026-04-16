#!/bin/bash
# SANKALP - Campus Management System - Unix/Linux/macOS Startup Script

echo ""
echo "========================================"
echo "    SANKALP - Campus Management System"
echo "========================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created!"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q

# Navigate to project
cd sankalp

# Apply migrations
echo "Applying migrations..."
python manage.py migrate --noinput

# Display options
echo ""
echo "========================================"
echo "What would you like to do?"
echo "========================================"
echo "1. Run Development Server"
echo "2. Create Superuser (Admin)"
echo "3. Run Tests"
echo "4. Collect Static Files"
echo "5. Exit"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "Starting development server..."
        echo "Access the application at: http://127.0.0.1:8000/"
        echo "Press CTRL+C to stop the server"
        echo ""
        python manage.py runserver
        ;;
    2)
        echo ""
        echo "Create Superuser (Admin)"
        python manage.py createsuperuser
        ;;
    3)
        echo ""
        echo "Running tests..."
        python manage.py test
        ;;
    4)
        echo ""
        echo "Collecting static files..."
        python manage.py collectstatic --noinput
        echo "Done!"
        ;;
    5)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Please try again."
        ;;
esac
