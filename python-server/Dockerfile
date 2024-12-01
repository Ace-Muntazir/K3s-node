# Use a lightweight Python base image
FROM python:3.9-alpine

# Set working directory
WORKDIR /app

# Copy only the necessary files first (helps with caching layers)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Specify the command to run the app
CMD ["python", "server.py"]

