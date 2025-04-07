# Use an official Python runtime as base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the app port
EXPOSE 8080

# Command to run the app
CMD ["python", "app.py"]
