# Use an official Python 3.12 slim image as the base image.
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy configuration files and install them via pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the working directory
COPY . /app

# Expose the port on which the application will run
EXPOSE 5000

# Set the environment variable used by the application
ENV APP_ENV production

# Command to run the application
CMD ["python", "main.py"]
