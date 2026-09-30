import xmlrpc.client
import os
from dotenv import dotenv_values

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env = dotenv_values(os.path.join(BASE_DIR, '.env'))

common = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/common', allow_none=True)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USERNAME'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/object', allow_none=True)

print("=== USER LIST ===")
users = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'res.users', 'read',
    [[5, 6, 7, 8, 9]],
    {'fields': ['id', 'name', 'login', 'email']}
)
for u in users:
    print(f"ID {u['id']}: {u['name']} (login: {u['login']})")

print("\n=== FIXING TASK 65 ===")
# Force task 65 to be assigned explicitly to Ebenezer (User 5) and Jason (User 6)
models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.task', 'write',
    [[65], {'user_ids': [(6, 0, [5, 6])]}]
)
print("Updated Task 65 to strictly assign to User 5 (Ebenezer) and User 6 (Jason).")
