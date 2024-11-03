FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV ROSSUM_USERNAME='rojec51441@evasud.com'
ENV ROSSUM_PASSWORD='qwedfgvbn123'
ENV POSTBIN_URL='https://www.postb.in/1730664247847-4251451964955'
ENV ROSSUM_DOMAIN='mspas.rossum.app'
# Create Django superuser (modify as necessary)
ENV DJANGO_SUPERUSER_USERNAME=myUser123
ENV DJANGO_SUPERUSER_PASSWORD=secretSecret

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Copy the application files
COPY . /app/

# Run database migrations and create superuser
RUN python manage.py migrate --noinput && python manage.py createsu
