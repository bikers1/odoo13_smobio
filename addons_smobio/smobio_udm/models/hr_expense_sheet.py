# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class HrExpenseSheet(models.Model):
    _name = "hr.expense.sheet"
    _inherit = ["hr.expense.sheet", "tier.validation"]
    _state_from = ["draft"]
    _state_to = ["submit", "approve", "post", "done"]

    def action_submit_sheet(self):
        super(HrExpenseSheet, self).action_submit_sheet()
        responsible_id = self.user_id.id or self.env.user.id
        self.write({'state': 'approve', 'user_id': responsible_id})
        self.activity_update()

    # def _compute_validated_rejected(self):
    #     super(HrExpenseSheet, self)._compute_validated_rejected()
    #     for rec in self:
    #         if rec.validated and rec.state == 'draft' and rec._name == 'hr.expense.sheet':
    #             # rec.action_submit_sheet()
    #             rec.write({'state': 'approve'})
    #             rec.activity_update()
