import xmlrpc.client
import os
from dotenv import dotenv_values

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env = dotenv_values(os.path.join(BASE_DIR, '.env'))

common = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/common', allow_none=True)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USERNAME'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/object', allow_none=True)

# Force custom fields on Task 65 to match a "GOOD" task
models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.task', 'write',
    [[65], {
        'x_task_level': 1,
        'state': '03_approved'
    }]
)
print("Updated Task 65 with custom fields.")
