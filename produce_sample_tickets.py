"""
Publishes fake ticket/incident events to a local Kafka topic, shaped exactly
like the real IncidentEvent.of(...) structure from the Kraken/FCM codebase.

Setup:
    pip install kafka-python
    docker compose up -d      # starts local Kafka on localhost:9094

Run:
    python produce_sample_tickets.py
"""

import json
import random
import time
from datetime import datetime, timedelta, timezone

from kafka import KafkaProducer

BOOTSTRAP_SERVERS = "localhost:9094"
TOPIC = "tickets"

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

STATUSES = ["OPEN", "ASSIGNED", "IN_PROGRESS", "RESOLVED", "CLOSED"]
PRIORITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
SEVERITIES = ["MINOR", "MAJOR", "CRITICAL"]
ASSIGNEES = ["supertech_erp", "Andy.Appiah", "Aisha.Frimpong"]
CATEGORIES = ["Network", "Hardware", "Software", "Access Request"]
REGIONS = ["Greater Accra", "Ashanti", "Western"]


def make_incident(ticket_num: int) -> dict:
    now = datetime.now(timezone.utc)
    due = now + timedelta(days=random.randint(1, 7))

    return {
        "id": str(ticket_num),
        "serviceRecordNumber": str(80000 + ticket_num),
        "owner": "system",
        "assignedTo": random.choice(ASSIGNEES),
        "dueDate": int(due.timestamp()),
        "priority": random.choice(PRIORITIES),
        "severity": random.choice(SEVERITIES),
        "status": random.choice(STATUSES),
        "contactPerson": "Jason Mi",
        "contactOnSite": "Site Contact",
        "description": f"Sample incident #{ticket_num} description",
        "cause": "",
        "solution": "",
        "createdTime": int(now.timestamp()),
        "createdBy": "system",
        "modifiedTime": int(now.timestamp()),
        "modifiedBy": "system",
        "thirdLevelName": "Level 3 Support",
        "subCategoryName": "Connectivity",
        "type": "Incident",
        "category": random.choice(CATEGORIES),
        "region": random.choice(REGIONS),
        "client": "Sample Client Ltd",
        "site": "Site A",
        "adminGroup": random.choice(["IT SUPPORT", "NETWORK OPERATIONS (NOC)", "APPLICATIONS", "CYBER"]),
    }


if __name__ == "__main__":
    # Create ONE ticket
    event = make_incident(3)
    producer.send(TOPIC, event)
    print(f"Created ticket {event['serviceRecordNumber']} (ID: {event['id']})")
    producer.flush()

    print("Waiting 5 seconds before sending an update...")
    time.sleep(5)

    # Update the same ticket
    event["status"] = "RESOLVED"
    event["priority"] = "CRITICAL"
    event["solution"] = "We fixed it by restarting the router."
    event["description"] += " [UPDATED]"
    event["modifiedTime"] = int(datetime.now(timezone.utc).timestamp())
    event["modifiedBy"] = "jason.admin"

    producer.send(TOPIC, event)
    print(f"Updated ticket {event['serviceRecordNumber']} -> status={event['status']}")
    
    producer.flush()
    print("Done. Check Odoo to see if the task was updated instead of duplicated.")
