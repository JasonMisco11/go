import json
import xmlrpc.client
from dotenv import dotenv_values

env = dotenv_values('.env')
common = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/common', allow_none=True)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USERNAME'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/object', allow_none=True)

# Fetch all internal users from Odoo
users = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'], 
    'res.users', 'search_read', 
    [[['share', '=', False]]], 
    {'fields': ['id', 'name', 'login']}
)

# Build a mapping dictionary
# We'll try to guess the Kraken username by formatting the Odoo name (e.g. "John Doe" -> "John.Doe")
mapping = {}
for u in users:
    # Try to generate a Kraken-like username as a helpful starting point
    guessed_kraken_name = u['name'].replace(" ", ".").replace("..", ".")
    
    mapping[guessed_kraken_name] = {
        "odoo_user_id": u['id'],
        "odoo_name": u['name'],
        "odoo_email": u['login']
    }

output = {
    "_instructions": "Change the keys (e.g., 'Andrews.O..Appiah') to match the exact username Kraken sends (e.g., 'Andy.Appiah').",
    "mapping": mapping
}

with open("user_mapping.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Generated user_mapping.json with {len(users)} Odoo users!")
