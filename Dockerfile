# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy files
COPY backend/ ./

# Install dependencies
RUN pip install -r requirements.txt

# Run API server
CMD ["python", "api.py"]
