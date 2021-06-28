# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Odoo 13 Taiwan Balance Sheet',
    'version': '13.0.1.0.2',
    'category': 'Invoicing Management',
    'summary': 'Taiwan Balance Sheet For Odoo 13',
    'sequence': '10',
    'description': """★技術支援：元植研究所""",
    'author': 'CHANG, CHING',
    'license': 'LGPL-3',
    'website': '',
    'depends': ['account', 'l10n_tw_standard_ifrss', 'accounting_pdf_reports'],
    'demo': [],
    'data': [
        'reports/report_financial_tw.xml',
        'reports/report.xml',

        'wizards/balance_sheet.xml',

        'views/account_reports_settings.xml',
        'data/account_financial_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'qweb': [],
}
