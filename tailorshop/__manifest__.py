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
    'depends': ['web','sale','product_custom_options'],
    'data': [
        'views/sales_view.xml',
        'views/product_view.xml',
        'reports/reports.xml',
        'reports/sale_report.xml',
        'wizards/measure_view.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False
}
