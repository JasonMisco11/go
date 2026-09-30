"""
DEFINITIVE TEST: Create the simplest possible task via API.
If this task shows up in the Odoo UI, the issue is with our complex fields.
If this task does NOT show up, the issue is at the project or Odoo level.
"""
import xmlrpc.client
import os
from dotenv import dotenv_values

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env = dotenv_values(os.path.join(BASE_DIR, '.env'))

common = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/common', allow_none=True)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USERNAME'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/object', allow_none=True)

print(f"Authenticated as uid={uid}")

# Get project IDs
kraken_id = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.project', 'search',
    [[('name', '=', 'Kraken - Applications')]]
)[0]

newproj_id = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.project', 'search',
    [[('name', '=', 'NewProj')]]
)[0]

# TEST 1: Simplest task in Kraken - Applications (just name + project)
task1 = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.task', 'create',
    [{'name': 'API TEST - Kraken Simple', 'project_id': kraken_id}]
)
print(f"\nCreated Task {task1} in 'Kraken - Applications' (minimal fields)")

# TEST 2: Simplest task in NewProj (just name + project)
task2 = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.task', 'create',
    [{'name': 'API TEST - NewProj Simple', 'project_id': newproj_id}]
)
print(f"Created Task {task2} in 'NewProj' (minimal fields)")

# Read them back to confirm
for tid in [task1, task2]:
    t = models.execute_kw(
        env['ODOO_DB'], uid, env['ODOO_API_KEY'],
        'project.task', 'read', [tid],
        {'fields': ['id', 'name', 'project_id', 'stage_id', 'active', 'user_ids', 'display_in_project']}
    )
    print(f"\n  Task {tid}: {t}")

print("\n>>> NOW GO CHECK ODOO:")
print(">>> 1. Does 'API TEST - Kraken Simple' show up in Kraken - Applications?")
print(">>> 2. Does 'API TEST - NewProj Simple' show up in NewProj?")
print(">>> If NEITHER shows up -> API/session issue")
print(">>> If only NewProj shows up -> Kraken project config issue")
print(">>> If BOTH show up -> issue is with our complex ticket fields")
