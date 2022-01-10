# -*- coding: utf-8 -*-

from odoo import api, models

class EmployeeAdvanceExpense(models.Model):
    _name = 'employee.advance.expense'
    _inherit = ['employee.advance.expense', 'tier.validation','mail.thread', 'mail.activity.mixin']
    _state_from = ["draft", "confirm"]
    _state_to = ["approved_hr_manager", "paid", "done"]

    @api.model
    def _get_under_validation_exceptions(self):
        res = super(EmployeeAdvanceExpense, self)._get_under_validation_exceptions()
        res.append("route_id")
        return res