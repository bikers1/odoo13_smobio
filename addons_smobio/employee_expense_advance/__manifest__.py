# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name': 'Expense Advance Request - Employee',
    'version': '1.0',
    'price': 25.0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'category': 'Human Resources',
    'summary': 'Expense Advance Request - Employee',
    'description': """
        Employee Advance Expense Requests:
            """,
    'support': 'contact@probuse.com',
    'images': ['static/description/img1.jpg'],
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'website': 'www.probuse.com',
    'depends': ['web','hr_expense'],
    'live_test_url': 'https://youtu.be/Mty6cj6O6Xw',
    'data': [
        'security/employee_advance_expense_security.xml',
             'security/ir.model.access.csv',
             'data/expense_sequence_data.xml',
             'views/employee_advance_expense.xml',
             'views/hr_expense.xml',
             'views/advance_expense_sheet.xml',
             'report/employee_advance_expense_report.xml'
             ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
