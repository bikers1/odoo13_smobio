# -*- coding: utf-8 -*-
# 本模組由元植管理顧問開發與維護，未經同意不得複製與散布

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    nhi_rate = fields.Float(string='健保局費率-雇員(%)', related='company_id.nhi_rate', readonly=False)
    nhi_host_rate = fields.Float(string='健保局費率-雇主、自營業主、自行職業(%)', related='company_id.nhi_host_rate', readonly=False)
    nhi_avg_f = fields.Float(string='健保局-平均眷口數(%)', related='company_id.nhi_avg_f', readonly=False)
    nhi2_rate = fields.Float(string='2代健保局費率(%)', related='company_id.nhi2_rate', readonly=False)
    bli_rate = fields.Float(string='勞保費率-勞工保險普通事故保險費率(%)', related='company_id.bli_rate', readonly=False)
    bli2_rate = fields.Float(string='勞保費率-就業保險費率(%)', related='company_id.bli2_rate', readonly=False)
    bli3_rate = fields.Float(string='勞保費率-勞工保險職業災害保險費(%)', related='company_id.bli3_rate', readonly=False)
    bli4_rate = fields.Float(string='勞保費率-勞工退休金(%)', related='company_id.bli4_rate', readonly=False)