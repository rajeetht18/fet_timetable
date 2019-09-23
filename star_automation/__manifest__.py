# -*- coding: utf-8 -*-


{
    'name': "Star Automation",
    'summary': """
        ERP Integration""",
    'description': """Star Automation""",
    "version"      : "0.6",
    "author"       : "Noble Johney",
    "website"      : "",
    'category': 'Accounting',
    'version': '1.1',
    'depends': ['base','hr_timesheet','crm','deltatech_service','hr','project','sale_crm','account','stock'],
    'data': [

        'views/user_view.xml',
        'views/crm_view.xml',
        'views/service_view.xml',
        'views/project_view.xml',
        'views/sale_report_templates.xml',
        'views/sales_view.xml',
        'data/crm_data.xml',
        'data/ir_sequence.xml',
        'views/menu.xml',
        'security/ir.model.access.csv'

    ],
    "auto_install" : False,
    "installable"  : True,
}
