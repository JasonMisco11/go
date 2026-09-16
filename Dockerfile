FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python scripts and JSON mapping files
COPY kraken_to_odoo_consumer.py .
COPY admin_group_to_odoo_department.json .
COPY ticket_type_to_odoo_issue_type.json .
COPY user_mapping.json .

# Set environment variables for data persistence
# (These will point to the mounted /app/data volume)
ENV DB_FILE_PATH="/app/data/kraken_odoo_sync.db"
ENV LOG_FILE_PATH="/app/data/sync.log"

# Run the consumer when the container launches
CMD ["python", "-u", "kraken_to_odoo_consumer.py"]
