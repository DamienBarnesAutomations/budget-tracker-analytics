# Use a slim version of Python
FROM python:3.11-slim

# Environment variables for better logging and efficiency
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install with a timeout to prevent local/render hangs
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Copy the rest of the application
COPY . .

# Ensure the script is executable and has Linux line endings
RUN chmod +x run.sh

# Streamlit/Render port
EXPOSE 10000

# Entry point
CMD ["./run.sh"]