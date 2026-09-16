"""
One-off helper: dump the valid selection values (and relation targets) for the
Odoo fields this integration needs, so PRIORITY_MAP / ISSUE_TYPE_MAP /
requestor_type can be filled in with real stored values instead of guesses.

Odoo selection fields store an internal value (e.g. "1", "low") that is often
different from the label you see in the UI (e.g. "Medium") - this script
prints both so there's no ambiguity.

Setup:
    export ODOO_URL="https://your-instance.odoo.com"
    export ODOO_DB="your-db-name"
    export ODOO_USERNAME="you@company.com"
    export ODOO_API_KEY="your-api-key"

Run:
    python get_odoo_selection_values.py
"""

import json
import os
import xmlrpc.client

from dotenv import load_dotenv

load_dotenv()

ODOO_URL = os.environ["ODOO_URL"]
ODOO_DB = os.environ["ODOO_DB"]
ODOO_USERNAME = os.environ["ODOO_USERNAME"]
ODOO_API_KEY = os.environ["ODOO_API_KEY"]

FIELDS_TO_CHECK = [
    "priority",         # native star-rating priority
    "x_priority",       # custom required priority selection
    "x_issue_type",     # custom required issue type selection
    "requestor_type",   # custom required request type selection
    "x_department_id",  # confirms the actual comodel (hr.department or custom)
]

common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_API_KEY, {})
if not uid:
    raise SystemExit("Odoo authentication failed - check ODOO_* env vars")

models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

fields_meta = models.execute_kw(
    ODOO_DB, uid, ODOO_API_KEY,
    "project.task", "fields_get",
    [FIELDS_TO_CHECK],
    {"attributes": ["string", "type", "selection", "relation"]},
)

print(json.dumps(fields_meta, indent=2))