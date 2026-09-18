"""
Publishes fake ticket/incident events to a local Kafka topic, shaped exactly
like the real IncidentEvent.of(...) structure from the Kraken/FCM codebase.

Setup:
    pip install kafka-python
    docker compose up -d      # starts local Kafka on localhost:9094

Run:
    python produce_sample_tickets.py
"""
####kraken here


import os
import json
import random
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import dotenv_values
from kafka import KafkaProducer

BASE_DIR = Path(__file__).resolve().parent.parent
env = dotenv_values(BASE_DIR / ".env")

BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS") or env.get("KAFKA_BOOTSTRAP_SERVERS") or "localhost:9094"
TOPIC = "tickets"

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

STATUSES = ["OPEN", "ASSIGNED", "IN_PROGRESS", "RESOLVED", "CLOSED"]
PRIORITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
SEVERITIES = ["MINOR", "MAJOR", "CRITICAL"]
ASSIGNEES = ["Chris Kwaku Bekor", "danielda@stlghana.com", "Jason Asamoah"]
CATEGORIES = ["Network", "Hardware", "Software", "Access Request"]
REGIONS = ["Eastern", "Volta", "Western"]


def make_incident(ticket_num: int) -> dict:
    now = datetime.now(timezone.utc)
    due = now + timedelta(days=random.randint(1, 7))

    return {
        "id": str(ticket_num),
        "serviceRecordNumber": str(90000 + ticket_num),
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
    print("Sending IT&DC test ticket for Jason...")
    event_jason = make_incident(407)
    event_jason["assignedTo"] = "jasonas@stlghana.com"            # <--- Update this to match Jason's Kraken username!
    event_jason["adminGroup"] = "IT & DC"         # Maps to IT&DC in your JSON
    event_jason["status"] = "OPEN"                    # This will create a closed ticket in Odoo
    producer.send(TOPIC, event_jason)
    print(f"Created ticket {event_jason['serviceRecordNumber']} for Jason")

    print("Sending Application test ticket for Daniel...")
    event_daniel = make_incident(409)
    event_daniel["assignedTo"] = "danielda@stlghana.com"            # <--- Update this to match Daniel's Kraken username!
    event_daniel["adminGroup"] = "APPLICATIONS"       # Maps to Application in your JSON
    event_daniel["status"] = "CLOSED"                   
    producer.send(TOPIC, event_daniel)
    print(f"Created ticket {event_daniel['serviceRecordNumber']} for Daniel")


    print("Sending IT&DC test ticket for Jason...")
    event_daniel = make_incident(410)
    event_daniel["assignedTo"] = "danielda@stlghana.com"            # <--- Update this to match Daniel's Kraken username!
    event_daniel["adminGroup"] = "APPLICATIONS"         # Maps to Application in your JSON
    event_daniel["status"] = "OPEN"                    # This will create an open ticket in Odoo
    producer.send(TOPIC, event_daniel)
    print(f"Created ticket {event_daniel['serviceRecordNumber']} for Daniel")






    producer.flush()
    print("Done! Check Odoo to see if both tasks were created with the correct departments and assignees.")
