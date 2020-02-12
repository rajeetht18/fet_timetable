# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'TailorShop',
    'version': '1.0',
    'category': 'Sales/Sales',
    'summary': 'Tailor Custom',
    'description': """
This module contains customisation of Tailor shop.
    """,
    'depends': ['sale'],
    'data': [
#        'views/sales_view.xml',
        'wizards/measure_view.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False
}

