FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the structured directories
COPY src/ src/
COPY config/ config/

# Set environment variables for data persistence
# (These will point to the mounted /app/data volume)
ENV DB_FILE_PATH="/app/data/kraken_odoo_sync.db"
ENV LOG_FILE_PATH="/app/data/sync.log"

# Run the consumer when the container launches
CMD ["python", "-u", "src/consumer.py"]
