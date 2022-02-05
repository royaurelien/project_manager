# -*- coding: utf-8 -*-
{
    'name': "Project ToDo",

    'summary': """Project ToDo""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Aurelien ROY",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'project',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/project_todo.xml',
        'views/project_todo_type.xml',
        'views/project_views.xml',
        'views/project_task_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
