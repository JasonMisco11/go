import xmlrpc.client
import os
from dotenv import dotenv_values

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env = dotenv_values(os.path.join(BASE_DIR, '.env'))

common = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/common', allow_none=True)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USERNAME'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/object', allow_none=True)

# 1. Get a task from "NewProj" (which shows tasks in UI)
print("=== GOOD TASK (From NewProj) ===")
good_tasks = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.task', 'search_read',
    [[('project_id.name', '=', 'NewProj')]],
    {'limit': 1}
)
good_task = good_tasks[0] if good_tasks else {}
print(f"ID: {good_task.get('id')}, Name: {good_task.get('name')}")

# 2. Get our API task (Task 65)
print("\n=== KRAKEN TASK (Task 65) ===")
api_tasks = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.task', 'search_read',
    [[('id', '=', 65)]],
    {'limit': 1}
)
api_task = api_tasks[0] if api_tasks else {}
print(f"ID: {api_task.get('id')}, Name: {api_task.get('name')}")

# 3. Compare fields
print("\n=== FIELD COMPARISON (Good Task vs Kraken Task) ===")
keys_to_ignore = ['id', 'name', 'project_id', 'create_date', 'write_date', 'message_follower_ids', 'message_ids', 'description']

if good_task and api_task:
    for key in good_task.keys():
        if key in keys_to_ignore:
            continue
        val_good = good_task.get(key)
        val_api = api_task.get(key)
        if val_good != val_api:
            # Only print if the good task actually has a meaningful value that we are missing
            if val_good and not val_api:
                print(f"MISSING IN KRAKEN: {key} = {val_good} (Kraken has {val_api})")
            elif val_good != val_api:
                pass # print(f"DIFFERENCE: {key} | Good: {val_good} | Kraken: {val_api}")
