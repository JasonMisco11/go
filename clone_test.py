import xmlrpc.client
import os
from dotenv import dotenv_values

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env = dotenv_values(os.path.join(BASE_DIR, '.env'))

common = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/common', allow_none=True)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USERNAME'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/object', allow_none=True)

print("=== CLONING A KNOWN GOOD TASK ===")

# 1. Find the known good task from NewProj (Task 31 from our previous test)
good_tasks = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.task', 'search_read',
    [[('id', '=', 31)]],
    {'limit': 1}
)

if not good_tasks:
    print("Could not find the good task (ID 31).")
    exit()

good_task = good_tasks[0]

# 2. Find the Kraken Applications project ID
kraken_proj_ids = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.project', 'search',
    [[('name', '=', 'Kraken - Applications')]]
)
kraken_proj_id = kraken_proj_ids[0] if kraken_proj_ids else False

# 3. Use Odoo's native 'copy' method to identically clone the good task, 
# but put it in the Kraken project.
new_task_id = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.task', 'copy',
    [good_task['id'], {
        'name': 'CLONED TASK FROM UI - SHOULD BE VISIBLE',
        'project_id': kraken_proj_id,
        'user_ids': [(6, 0, [5, 6, 8])], # Assign to Ebenezer (8), Jason (6), and Daniel (5)
        'stage_id': 22 # Backlog
    }]
)

print(f"Successfully cloned task! New Task ID: {new_task_id}")
print("Please check Odoo -> Kraken - Applications to see if 'CLONED TASK FROM UI' appears.")
