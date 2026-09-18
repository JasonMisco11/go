import xmlrpc.client
from dotenv import dotenv_values

env = dotenv_values('.env')
common = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/common', allow_none=True)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USERNAME'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/object', allow_none=True)

# First get the Kraken project ID
project_ids = models.execute_kw(env['ODOO_DB'], uid, env['ODOO_API_KEY'], 'project.project', 'search', [[('name', '=', 'Kraken - IT & DC')]])
if not project_ids:
    print("Project 'Kraken - IT & DC' not found!")
    exit(1)
project_id = project_ids[0]

# Now get the stages available for this project
stages = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'], 
    'project.task.type', 'search_read', 
    [[]], # We'll just fetch all stages and filter, or filter by project_ids
    {'fields': ['id', 'name', 'project_ids']}
)

print(f"--- STAGES FOR PROJECT 'Kraken' (ID: {project_id}) ---")
for s in stages:
    # Odoo stages can be global (project_ids is empty) or project-specific
    if not s['project_ids'] or project_id in s['project_ids']:
        print(f"Stage ID: {s['id']} | Name: {s['name']}")
