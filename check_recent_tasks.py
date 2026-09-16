import xmlrpc.client
from dotenv import dotenv_values
env = dotenv_values('.env')
common = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/common', allow_none=True)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USERNAME'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/object', allow_none=True)

# Find the most recently updated tasks in the Kraken project
tasks = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.task', 'search_read',
    [[['project_id.name', '=', 'Kraken']]],
    {'fields': ['id', 'name', 'stage_id', 'priority', 'x_priority'], 'order': 'write_date desc', 'limit': 3}
)

print("\n--- RECENT KRAKEN TASKS ---")
for t in tasks:
    print(t)
