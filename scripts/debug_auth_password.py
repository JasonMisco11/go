"""Try authenticating with a manually entered password to isolate API key vs password issue."""

import getpass
import xmlrpc.client

from dotenv import load_dotenv
import os

load_dotenv()

url = os.environ["ODOO_URL"]
db = os.environ["ODOO_DB"]
username = os.environ["ODOO_USERNAME"]

print(f"Odoo: {url}  DB: {db}  User: {username}")
print()

# Try 1: existing API key from .env
api_key = os.environ.get("ODOO_API_KEY", "")
if api_key:
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, api_key, {})
    print(f"Try 1 — API key from .env: {'✓ uid=' + str(uid) if uid else '✗ Failed'}")
else:
    print("Try 1 — No API key in .env, skipped")

# Try 2: prompt for login password
print()
password = getpass.getpass("Enter your Odoo login password (the one you type in the browser): ")
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
print(f"Try 2 — Login password:    {'✓ uid=' + str(uid) if uid else '✗ Failed'}")

if uid:
    print()
    print("==> Your login password works! Update .env:")
    print(f"    ODOO_API_KEY={password}")
    print()
    print("Or better: generate a fresh API key in Odoo:")
    print(f"  1. Log into {url}")
    print("  2. Click your avatar (top right) → My Profile → Account Security")
    print("  3. Under 'API Keys' → New API Key")
    print("  4. Copy the key and put it in .env as ODOO_API_KEY")
