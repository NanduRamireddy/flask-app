# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and static files
COPY app.py app.py
COPY static/ static/
COPY templates/ templates/

# Expose the new port
EXPOSE 5001

# Run the application
CMD ["python", "app.py"]
