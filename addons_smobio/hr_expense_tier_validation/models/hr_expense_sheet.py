# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrExpenseSheet(models.Model):
    _name = "hr.expense.sheet"
    _inherit = ["hr.expense.sheet", "tier.validation"]
    _state_from = ["draft"]
    _state_to = ["submit", "approve", "post", "done"]

    def action_submit_sheet(self):
        super(HrExpenseSheet, self).action_submit_sheet()
        if self.validated:
            self.write({'state': 'approve'})
            self.activity_update()