# Use Python Alpine image
FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache g++ curl


# Copy application files
COPY ./ /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Run the application
ENTRYPOINT ["python3", "entrypoint.py"]