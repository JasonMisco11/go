"""
Forensic comparison: Dump ALL fields from a visible task vs an invisible Kraken task.
This will tell us exactly what field is causing the invisibility.
"""
import xmlrpc.client
import os
from dotenv import dotenv_values

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env = dotenv_values(os.path.join(BASE_DIR, '.env'))

common = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/common', allow_none=True)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USERNAME'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/object', allow_none=True)

# Get one WORKING task from NewProj (which shows 3 tasks in the UI)
good_ids = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.task', 'search',
    [[('project_id.name', '=', 'NewProj')]],
    {'limit': 1}
)

# Get one BROKEN task from Kraken
bad_ids = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.task', 'search',
    [[('project_id.name', '=', 'Kraken - Applications')]],
    {'limit': 1}
)

if not good_ids:
    print("ERROR: No tasks found in NewProj!")
elif not bad_ids:
    print("ERROR: No tasks found in Kraken - Applications via API search!")
    # Try without project filter
    print("Trying direct ID lookup for task 65...")
    bad_ids = [65]

print(f"Good task ID: {good_ids[0] if good_ids else 'NONE'}")
print(f"Bad task ID:  {bad_ids[0] if bad_ids else 'NONE'}")

# Read ALL fields from both (passing empty list = all fields)
good_task = {}
bad_task = {}

if good_ids:
    result = models.execute_kw(
        env['ODOO_DB'], uid, env['ODOO_API_KEY'],
        'project.task', 'read', [good_ids[0]]
    )
    good_task = result[0] if isinstance(result, list) else result

if bad_ids:
    result = models.execute_kw(
        env['ODOO_DB'], uid, env['ODOO_API_KEY'],
        'project.task', 'read', [bad_ids[0]]
    )
    bad_task = result[0] if isinstance(result, list) else result

# Critical fields to check first
critical_fields = ['active', 'project_id', 'stage_id', 'company_id', 'user_ids', 
                   'personal_stage_type_ids', 'display_in_project', 'parent_id',
                   'ancestor_id', 'is_private']

print("\n" + "="*60)
print("CRITICAL FIELD COMPARISON")
print("="*60)
for field in critical_fields:
    gv = good_task.get(field, 'FIELD_NOT_FOUND')
    bv = bad_task.get(field, 'FIELD_NOT_FOUND')
    marker = "  ✓" if gv == bv else "  ✗ DIFFERENT!"
    print(f"\n  {field}:")
    print(f"    GOOD (NewProj):  {gv}")
    print(f"    BAD  (Kraken):   {bv}{marker}")

# Now dump ALL differences
print("\n" + "="*60)
print("ALL FIELD DIFFERENCES")
print("="*60)
skip = {'id', 'name', 'create_date', 'write_date', 'message_ids', 
        'message_follower_ids', 'activity_ids', 'description',
        'date_last_stage_update', '__last_update', 'display_name'}

if good_task and bad_task:
    all_keys = set(good_task.keys()) | set(bad_task.keys())
    for key in sorted(all_keys):
        if key in skip:
            continue
        gv = good_task.get(key)
        bv = bad_task.get(key)
        if gv != bv:
            print(f"\n  {key}:")
            print(f"    GOOD: {gv}")
            print(f"    BAD:  {bv}")
