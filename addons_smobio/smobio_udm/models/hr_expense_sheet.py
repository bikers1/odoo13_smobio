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

class HrExpense(models.Model):
    _inherit = "hr.expense"

    @api.model
    def _get_employee_id_domain(self):
        res = "['|', ('company_id', '=', False), ('company_id', '=', company_id)]"  # Then, domain accepts everything
        # res = [('id', '=', 0)] # Nothing accepted by domain, by default
        # if self.user_has_groups('hr_expense.group_hr_expense_user') or self.user_has_groups('account.group_account_user'):
        #     res = "['|', ('company_id', '=', False), ('company_id', '=', company_id)]"  # Then, domain accepts everything
        # elif self.user_has_groups('hr_expense.group_hr_expense_team_approver') and self.env.user.employee_ids:
        #     user = self.env.user
        #     employee = self.env.user.employee_id
        #     res = [
        #         '|', '|', '|',
        #         ('department_id.manager_id', '=', employee.id),
        #         ('parent_id', '=', employee.id),
        #         ('id', '=', employee.id),
        #         ('expense_manager_id', '=', user.id),
        #         '|', ('company_id', '=', False), ('company_id', '=', employee.company_id.id),
        #     ]
        # elif self.env.user.employee_id:
        #     employee = self.env.user.employee_id
        #     res = [('id', '=', employee.id), '|', ('company_id', '=', False), ('company_id', '=', employee.company_id.id)]
        return res