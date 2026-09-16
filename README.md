# Kraken to Odoo Integration

This service automatically listens to a Kafka topic for incoming IT tickets from the **Kraken** ticketing system and synchronizes them directly into **Odoo**. It handles both creating new tasks and updating existing ones.

## 🚀 Key Features

* **Dynamic Project Routing:** Automatically sorts tickets into specific Odoo Projects (e.g., `Kraken - IT`, `Kraken - Applications`) based on the Kraken `adminGroup`.
* **Smart User Resolution:** No need to manually map every single user! The script intelligently searches Odoo for the assignee by checking their **Email**, **Login/Username**, and **Full Name**.
* **Idempotency (No Duplicates):** Uses a local SQLite database (`kraken_odoo_sync.db`) to remember which Kraken ticket belongs to which Odoo task. If an update comes in for a ticket, it updates the existing Odoo task instead of creating a duplicate.
* **Dead Letter Queue (Safety Net):** If Odoo rejects a ticket (e.g., due to strict Timesheet rules), the script catches the crash and saves the entire ticket payload and the error message into the `failed_tickets` SQLite table so it is never lost.

---

## ⚙️ Configuration

### 1. Environment Variables (`.env`)
Create a `.env` file in the root directory with your production credentials:
```env
KAFKA_BOOTSTRAP_SERVERS="192.168.251.152:9094"
ODOO_URL="http://192.168.250.209:8079"
ODOO_DB="odoo19"
ODOO_USERNAME="jasonas@stlghana.com"
ODOO_API_KEY="your-api-key-here"
```

### 2. Project Routing (`kraken_to_odoo_consumer.py`)
To route tickets to different Odoo projects based on their Kraken department, update the `PROJECT_MAP` dictionary at the top of the python script:
```python
PROJECT_MAP = {
    "IT SUPPORT": "Kraken - IT",
    "APPLICATIONS": "Kraken - Applications",
}
```

### 3. User Overrides (`user_mapping.json`)
If a Kraken username is completely different from their Odoo email or name, you can manually override it here. 
*Note: You can use `python generate_user_mapping.py` to download all Odoo users and their IDs if you need to look them up.*

---

## 💻 How to Run

### Local Development / Testing
To run the consumer directly in your terminal:
```bash
python kraken_to_odoo_consumer.py
```
To send a fake ticket to test the routing and assignment:
```bash
python produce_sample_tickets.py
```

### Production (Docker)
To run this script 24/7 on your production server:
1. Ensure Docker is installed on the server.
2. Run the following command in the project folder:
```bash
docker compose -f docker-compose.prod.yml up -d --build
```
3. To view the live logs in production:
```bash
docker logs -f odoo_kraken_consumer
```

---

## 🛠️ Troubleshooting & Things to Know

* **"I deleted a task in Odoo for testing, and now the script crashes!"**
  The script remembers the old task ID in its local memory. Stop the script, delete the `kraken_odoo_sync.db` file, and restart. It will create fresh tasks.
* **"The Assignee field is blank in Odoo!"**
  Check `sync.log`. You will likely see `WARNING No Odoo user found for assignedTo...`. This means the Kraken username didn't match any Odoo email, login, or name. Add an override in `user_mapping.json` to fix it.
* **"A ticket didn't show up in Odoo at all!"**
  Open the SQLite database (`kraken_odoo_sync.db`) and look at the `failed_tickets` table. Odoo likely rejected it because of a required field or a business rule.
