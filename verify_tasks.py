"""Quick test: verify stage lookup works for each Kraken project."""
import xmlrpc.client
import os
from dotenv import dotenv_values

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env = dotenv_values(os.path.join(BASE_DIR, '.env'))

common = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/common', allow_none=True)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USERNAME'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/object', allow_none=True)

# 1. List ALL projects and their IDs
print("=== ALL PROJECTS ===")
projects = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.project', 'search_read', [[]],
    {'fields': ['id', 'name', 'task_count']}
)
for p in projects:
    print(f"  ID={p['id']}  name='{p['name']}'  tasks={p['task_count']}")

# 2. List ALL stages and which projects they belong to
print("\n=== ALL STAGES ===")
stages = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.task.type', 'search_read', [[]],
    {'fields': ['id', 'name', 'project_ids']}
)
for s in stages:
    print(f"  ID={s['id']}  name='{s['name']}'  projects={s['project_ids']}")

# 3. Test dynamic stage lookup for each Kraken project
print("\n=== STAGE LOOKUP TEST ===")
kraken_projects = ["Kraken - Applications", "Kraken - IT & DC", "Kraken Testing"]
test_stage = "Backlog"

for proj_name in kraken_projects:
    proj_ids = models.execute_kw(
        env['ODOO_DB'], uid, env['ODOO_API_KEY'],
        'project.project', 'search', [[("name", "=", proj_name)]]
    )
    if not proj_ids:
        print(f"  Project '{proj_name}' NOT FOUND")
        continue
    
    pid = proj_ids[0]
    domain = [("project_ids", "in", [pid]), ("name", "=", test_stage)]
    found = models.execute_kw(
        env['ODOO_DB'], uid, env['ODOO_API_KEY'],
        'project.task.type', 'search_read',
        [domain],
        {'fields': ['id', 'name']}
    )
    if found:
        print(f"  Project '{proj_name}' (id={pid}) -> '{test_stage}' stage_id={found[0]['id']} ✓")
    else:
        print(f"  Project '{proj_name}' (id={pid}) -> '{test_stage}' NOT FOUND ✗")

# 4. Show recent tasks with no stage
print("\n=== TASKS WITHOUT STAGE (potential invisible tasks) ===")
tasks = models.execute_kw(
    env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.task', 'search_read',
    [[("id", ">=", 60)]],
    {'fields': ['id', 'name', 'project_id', 'stage_id', 'user_ids'], 'order': 'id desc', 'limit': 10}
)
for t in tasks:
    print(f"  Task {t['id']}: '{t['name']}' project={t['project_id']} stage={t['stage_id']} users={t['user_ids']}")
