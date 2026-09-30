import xmlrpc.client
import os
from dotenv import dotenv_values

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env = dotenv_values(os.path.join(BASE_DIR, '.env'))

common = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/common', allow_none=True)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USERNAME'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/object', allow_none=True)

# Find all record rules applied to project.task
rules = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'ir.rule', 'search_read',
    [[('model_id.model', '=', 'project.task')]],
    {'fields': ['name', 'domain_force', 'groups']}
)

print("=== RECORD RULES FOR project.task ===")
for r in rules:
    print(f"\nRule: {r['name']}")
    print(f"Domain: {r['domain_force']}")
    print(f"Groups: {r['groups']}")
