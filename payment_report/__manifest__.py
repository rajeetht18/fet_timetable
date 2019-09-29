# -*- coding: utf-8 -*-


{
    'name': "Payment Report Customisation",
    'summary': """
        ERP Integration""",
    'description': """Payment Report Customisations""",
    "version"      : "0.1",
    "author"       : "Noble Johney",
    "website"      : "",
    'category': 'Accounting',
    'version': '1.1',
    'depends': ['base','account'],
    'data': [

        'views/report_template.xml',

    ],
    "auto_install" : False,
    "installable"  : True,
}
