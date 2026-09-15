"""Quick debug script to isolate the Odoo auth failure."""

import os
import xmlrpc.client

from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("ODOO_URL", "(not set)")
db = os.environ.get("ODOO_DB", "(not set)")
username = os.environ.get("ODOO_USERNAME", "(not set)")
api_key = os.environ.get("ODOO_API_KEY", "(not set)")

print("=== Loaded from .env ===")
print(f"  ODOO_URL      = {url}")
print(f"  ODOO_DB       = {db}")
print(f"  ODOO_USERNAME = {username}")
print(f"  ODOO_API_KEY  = {api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else f"  ODOO_API_KEY  = {api_key}")
print()

# Step 1: Can we reach the XML-RPC endpoint?
print("Step 1: Connecting to XML-RPC common endpoint...")
try:
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    version = common.version()
    print(f"  ✓ Connected — Odoo server version: {version.get('server_version', '?')}")
except Exception as e:
    print(f"  ✗ Cannot reach XML-RPC endpoint: {e}")
    raise SystemExit(1)

# Step 2: Try authenticate
print("\nStep 2: Authenticating...")
try:
    uid = common.authenticate(db, username, api_key, {})
    print(f"  Result: uid = {uid}  (type: {type(uid).__name__})")
    if uid:
        print(f"  ✓ Authenticated as uid {uid}")
    else:
        print("  ✗ authenticate() returned False/0 — bad credentials or user not found")
        print()
        print("  Possible causes:")
        print("    - API key is wrong or expired (regenerate in Odoo: Settings > Users > API Keys)")
        print("    - Username doesn't exist in this database")
        print("    - Password auth might be needed instead of API key (try your login password)")
        print("    - The user account is archived/inactive")
except Exception as e:
    print(f"  ✗ authenticate() raised an exception: {e}")

# Step 3: If auth worked, do a quick sanity check
if uid:
    print("\nStep 3: Quick sanity check — reading project list...")
    try:
        models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
        projects = models.execute_kw(db, uid, api_key, "project.project", "search_read", [[]], {"fields": ["name"], "limit": 5})
        print(f"  ✓ Found {len(projects)} project(s):")
        for p in projects:
            print(f"    - [{p['id']}] {p['name']}")
    except Exception as e:
        print(f"  ✗ Read failed: {e}")
