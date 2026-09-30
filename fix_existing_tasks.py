import xmlrpc.client
import os
from dotenv import dotenv_values

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env = dotenv_values(os.path.join(BASE_DIR, '.env'))

common = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/common', allow_none=True)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USERNAME'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/object', allow_none=True)

# Find all recent Kraken tasks
tasks = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.task', 'search_read',
    [[("id", ">=", 60)]],
    {'fields': ['id', 'user_ids']}
)

for t in tasks:
    task_id = t['id']
    current_users = t['user_ids']
    
    # Add Jason (uid) to the task if he isn't already there
    if uid not in current_users:
        new_users = list(set(current_users + [uid]))
        models.execute_kw(
            env['ODOO_DB'], uid, env['ODOO_API_KEY'],
            'project.task', 'write',
            [[task_id], {'user_ids': [(6, 0, new_users)]}]
        )
        print(f"Fixed Task {task_id}: Added you to the assignees so you can see it!")
    else:
        print(f"Task {task_id} is already visible to you.")

print("Done! Go check the Odoo board now.")
