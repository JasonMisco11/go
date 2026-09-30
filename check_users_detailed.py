import xmlrpc.client
import os
from dotenv import dotenv_values

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env = dotenv_values(os.path.join(BASE_DIR, '.env'))

common = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/common', allow_none=True)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USERNAME'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/object', allow_none=True)

users = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'res.users', 'read',
    [[5, 6, 7, 8, 9]],
    {'fields': ['id', 'name', 'login', 'email']}
)

print("=== USER LIST ===")
for u in users:
    print(f"ID {u['id']}: {u['name']} (login: {u['login']}, email: {u.get('email')})")
