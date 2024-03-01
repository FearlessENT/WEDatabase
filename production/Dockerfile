# Use the official Python image as a base
FROM python:3.8

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Install system dependencies, including MySQL client
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*



# Create and set the working directory inside the container
WORKDIR /app

# Install the Python dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of your Django project into the container
COPY manage.py .
COPY WEData/ WEData/


# Copy the entrypoint script and make it executable
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh


# Set the entrypoint script to be executed
ENTRYPOINT ["entrypoint.sh"]


# Expose the port the app runs on
EXPOSE 8000

RUN echo "running gunicorn"
# Start the Django development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "WEData.wsgi:application", "--bind", "0.0.0.0:8000"]

