# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang, format_date

INV_LINES_PER_STUB = 9


class AccountPayment(models.Model):
    _inherit = "account.payment"

    # check_number = fields.Char(readonly=False)


    def do_print_checks(self):
        """ This method is a hook for l10n_xx_check_printing modules to implement actual check printing capabilities """
        # raise UserError(_("You have to choose a check layout. For this, go in Apps, search for 'Checks layout' and install one."))


    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        if hasattr(super(AccountPayment, self), '_onchange_journal_id'):
            super(AccountPayment, self)._onchange_journal_id()
        if self.journal_id.check_manual_sequencing:
            self.check_number =self.journal_id.check_sequence_id.prefix+ str(self.journal_id.check_sequence_id.number_next_actual)