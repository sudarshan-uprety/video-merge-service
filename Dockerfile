# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install FFmpeg and other necessary packages
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary files to reduce image size
COPY ./app ./app
COPY ./utils ./utils
COPY ./main.py .
COPY ./Dockerfile .
COPY ./docker-compose.yml .
COPY ./requirements.txt .

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
