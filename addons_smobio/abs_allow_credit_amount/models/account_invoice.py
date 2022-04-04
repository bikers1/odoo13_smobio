# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import UserError,ValidationError

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        result= super(AccountMove,self).action_post()
        if self.partner_id:
            invoice_ids = self.env['account.move'].search([('partner_id','=', self.partner_id.id),('invoice_payment_state','!=','paid'),('state','!=','draft')])
            amount_total = 0
            for record in invoice_ids:
                amount_total =amount_total + record.amount_residual
            if self.partner_id.allowed_credit_amount == 0: 
                pass 
            elif self.partner_id.allowed_credit_amount < amount_total:
                raise ValidationError('Allowed credit amount is exceeded for this customer.')
            
