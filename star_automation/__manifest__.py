# -*- coding: utf-8 -*-


{
    'name': "Star Automation",
    'summary': """
        ERP Integration""",
    'description': """Star Automation""",
    "version"      : "0.4",
    "author"       : "Noble Johney",
    "website"      : "",
    'category': 'Accounting',
    'version': '1.1',
    'depends': ['base','crm','deltatech_service','hr','project'],
    'data': [

        'views/user_view.xml',
        'views/crm_view.xml',
        'views/service_view.xml',
        'views/project_view.xml',
        'data/crm_data.xml',
        'data/ir_sequence.xml',
        'views/menu.xml',

    ],
    "auto_install" : False,
    "installable"  : True,
}
