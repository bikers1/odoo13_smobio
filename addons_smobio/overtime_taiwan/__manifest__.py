# -*- coding: utf-8 -*-
{
    "name": "臺灣人力資源系統",
    "category": 'Human Resources',
    "summary": """
            加班費模組
        """,
    "description": """
            處理加班申請以及加班補休
        """,
    "sequence": 1,
    "version": '1.0',
    "depends": ['om_hr_payroll', 'hr_attendance'],
    "data": [
        'security/overtime_security.xml',
        'security/ir.model.access.csv',
        'views/dev_overtime_request.xml',
        'views/ir_sequence_data.xml',
        'views/demo_data.xml',
        'views/pay_slip_view.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
