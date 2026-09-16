import xmlrpc.client
from dotenv import dotenv_values

env = dotenv_values('.env')
common = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/common', allow_none=True)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USERNAME'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(env['ODOO_URL'] + '/xmlrpc/2/object', allow_none=True)

dept_ids = models.execute_kw(env['ODOO_DB'], uid, env['ODOO_API_KEY'], 'hr.department', 'search', [[]])
depts = models.execute_kw(env['ODOO_DB'], uid, env['ODOO_API_KEY'], 'hr.department', 'read', [dept_ids], {'fields': ['id', 'name']})
print('DEPARTMENTS:')
for d in depts:
    print(f" - {d['name']}")

issue_type_ids = models.execute_kw(env['ODOO_DB'], uid, env['ODOO_API_KEY'], 'project.task.issue.type', 'search', [[]])
issue_types = models.execute_kw(env['ODOO_DB'], uid, env['ODOO_API_KEY'], 'project.task.issue.type', 'read', [issue_type_ids], {'fields': ['id', 'name']})
print('\nISSUE TYPES:')
for t in issue_types:
    print(f" - {t['name']}")
