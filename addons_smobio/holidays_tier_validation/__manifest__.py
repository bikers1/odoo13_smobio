# -*- coding: utf-8 -*-
{
    "name": "Holidays Tier Validation",
    "summary": "Extends the functionality of Holidays support a tier validation process.",
    "version": "13.0.1.0.0",
    "category": "Human Resources",
    "depends": ["hr_holidays", "hr_org_chart", "base_tier_validation"],

    "data": [
        "views/hr_leave_view_form.xml",
        "views/hr_leave_allocation_view_form.xml"
    ],

    "installable": True,
    "application": True,
    "auto_install": False,
}
