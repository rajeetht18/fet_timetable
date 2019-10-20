# -*- coding: utf-8 -*-


{
    'name': "IndiaMart Integration",
    'summary': """
        ERP Integration""",
    'description': """IndiaMart Integration""",
    "version"      : "0.1",
    "author"       : "Noble Johney",
    "website"      : "",
    'category': 'Accounting',
    'depends': ['base','crm'],
    'data': [

        'views/settings_view.xml',
        'views/scheduler.xml',
        # 'security/ir.model.access.csv'

    ],
    "auto_install" : False,
    "installable"  : True,
}
