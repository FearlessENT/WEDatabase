# Use the official Python image as a base
FROM python:3.8

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies, including MySQL client and Apache with mod_wsgi
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    apache2 \
    apache2-dev \
    vim \
    && rm -rf /var/lib/apt/lists/* \
    && pip install mod_wsgi

# Create and set the working directory inside the container
WORKDIR /app

# Install the Python dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your Django project into the container
COPY manage.py .
COPY WEData/ WEData/

# Setup mod_wsgi
RUN apt-get update && apt-get install -y libapache2-mod-wsgi-py3
RUN a2enmod wsgi
RUN mod_wsgi-express install-module > /etc/apache2/mods-available/wsgi_express.load
RUN echo "LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so" > /etc/apache2/mods-available/wsgi.load

# Copy the Apache configuration file
# Make sure to create an apache.conf file as per the previous instructions
COPY apache.conf /etc/apache2/sites-available/000-default.conf


# Copy the entrypoint script and make it executable
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Expose the port the app runs on
EXPOSE 80

# Set the entrypoint script to be executed
ENTRYPOINT ["entrypoint.sh"]

# Configure Apache to run in the foreground
CMD ["apache2ctl", "-D", "FOREGROUND"]
