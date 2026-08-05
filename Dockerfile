# Use an official, lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker caching layers
COPY requirements.txt .

# Install the requests package
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY *.py .
EXPOSE 443
# Run the script when the container launches
CMD ["python", "main.py"]
