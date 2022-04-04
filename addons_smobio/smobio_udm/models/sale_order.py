# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    employee_id = fields.Many2one('hr.employee', string='員工', compute='_compute_company_employee',store=True)

    @api.depends('user_id')
    def _compute_company_employee(self):
        for user in self:
            user.employee_id = user.user_id.employee_id.id