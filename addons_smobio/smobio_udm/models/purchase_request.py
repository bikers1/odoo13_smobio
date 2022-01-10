# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class PurchaseRequest(models.Model):
    _name = "purchase.request"
    _inherit = ["purchase.request", "tier.validation"]
    _state_from = ["draft"]
    _state_to = ["approved","to_approve","done"]

    @api.returns('self')
    def _default_employee_get(self):
        return self.env.user.employee_id

    employee_id = fields.Many2one('hr.employee', string='員工', compute='_compute_company_employee',store=True)
    total_amount = fields.Monetary("金額合計", compute='_compute_amount', store=True, currency_field='currency_id')
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 states={'draft': [('readonly', False)], 'refused': [('readonly', False)]},
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True,
                                  states={'draft': [('readonly', False)], 'refused': [('readonly', False)]},
                                  default=lambda self: self.env.company.currency_id)

    @api.depends('line_ids.estimated_cost')
    def _compute_amount(self):
        for request in self:
            request.total_amount = sum(request.line_ids.mapped('estimated_cost'))

    @api.depends('requested_by')
    def _compute_company_employee(self):
        for user in self:
            user.employee_id = user.requested_by.employee_id.id