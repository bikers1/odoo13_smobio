# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class AccountFinancialReport(models.Model):
    _inherit = "account.financial.report"

    position = fields.Char(string='帳戶式報表位置', default='N')
