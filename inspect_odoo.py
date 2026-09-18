import xmlrpc.client
from dotenv import dotenv_values

env = dotenv_values('.env')
common = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/common', allow_none=True)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USERNAME'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/object', allow_none=True)

depts = models.execute_kw(env['ODOO_DB'], uid, env['ODOO_API_KEY'], 'hr.department', 'search_read', [[]], {'fields': ['id', 'name']})
print("Actual Odoo Departments:")
for d in depts:
    print(f"ID: {d['id']} | Name: '{d['name']}'")
