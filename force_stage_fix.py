import xmlrpc.client
import os
from dotenv import dotenv_values

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env = dotenv_values(os.path.join(BASE_DIR, '.env'))

common = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/common', allow_none=True)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USERNAME'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/object', allow_none=True)

# Find all recent Kraken tasks that might be broken
tasks = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.task', 'search_read',
    [[("id", ">=", 60)]],
    {'fields': ['id', 'project_id', 'stage_id']}
)

for t in tasks:
    task_id = t['id']
    project = t.get('project_id')
    if not project:
        continue
    project_id = project[0]
    
    # 1. Look up the proper stage ID for this project
    stages = models.execute_kw(
        env['ODOO_DB'], uid, env['ODOO_API_KEY'],
        'project.task.type', 'search_read',
        [[("project_ids", "in", [project_id]), ("name", "=", "Backlog")]],
        {'fields': ['id'], 'limit': 1}
    )
    
    if stages:
        stage_id = stages[0]['id']
        # 2. Update the task to attach it to the visible Kanban column
        models.execute_kw(
            env['ODOO_DB'], uid, env['ODOO_API_KEY'],
            'project.task', 'write',
            [[task_id], {'stage_id': stage_id}]
        )
        print(f"Fixed Task {task_id}: Successfully snapped it to the Backlog column!")

print("All tasks are fixed! Go refresh your Odoo board.")
