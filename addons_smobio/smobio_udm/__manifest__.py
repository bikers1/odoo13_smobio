# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'smobio 鴻林堂 客製模組',
    'version': '13.0',
    'category': 'tools',
    'description': """
    """,
    'depends': ['purchase_request', 'purchase_request_tier_validation','sale'],
    'data': [
        "security/employee_advance_expense_security.xml",
        "views/purchase_request_view.xml",
        "views/employee_advance_expense.xml",
        "views/sale_order_view.xml",
    ],
    'installable': True,
}
