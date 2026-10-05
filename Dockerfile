# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies if needed (for c-extensions)
# RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Create a virtual environment to isolate dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir pip==23.3.2 setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Production image
FROM python:3.11-slim

# Prevent Python from writing pyc files and buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    DB_FILE_PATH="/app/data/kraken_odoo_sync.db" \
    LOG_FILE_PATH="/app/data/sync.log"

WORKDIR /app

# Create a non-root user and group for security
ARG UID=10001
RUN addgroup --system --gid ${UID} appgroup && \
    adduser --system --uid ${UID} --ingroup appgroup appuser && \
    mkdir -p /app/data && \
    chown -R appuser:appgroup /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application code and set ownership
COPY --chown=appuser:appgroup kraken_to_odoo_consumer.py .
COPY --chown=appuser:appgroup admin_group_to_odoo_department.json .
COPY --chown=appuser:appgroup ticket_type_to_odoo_issue_type.json .
COPY --chown=appuser:appgroup user_mapping.json .

# Switch to the non-root user
USER appuser

# Run the consumer
CMD ["python", "kraken_to_odoo_consumer.py"]
