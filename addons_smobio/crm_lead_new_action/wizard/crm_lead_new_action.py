# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from odoo.exceptions import UserError, ValidationError


class Lead2OpportunityMassConvert(models.TransientModel):

    _inherit = 'crm.lead2opportunity.partner.mass'

    prefix = fields.Char(string='商機名稱前綴')
    suffix = fields.Char(string='商機名稱後綴')

    @api.model
    def default_get(self, fields):
        record_ids = self._context.get('active_ids')
        result = super().default_get(fields)

        if record_ids:
            if 'opportunity_ids' in fields:
                opp_ids = self.env['crm.lead'].browse(record_ids).filtered(
                    lambda opp: opp.probability < 100).ids
                result['opportunity_ids'] = opp_ids

        return result

    @api.onchange('user_id')
    def _onchange_user(self):
        if self.user_id:
            if self.team_id:
                user_in_team = self.env['crm.team'].search_count([('id', '=', self.team_id.id), '|', (
                    'user_id', '=', self.user_id.id), ('member_ids', '=', self.user_id.id)])
            else:
                user_in_team = False
            if not user_in_team:
                values = self.env['crm.lead']._onchange_user_values(
                    self.user_id.id if self.user_id else False)
                self.team_id = values.get('team_id', False)

    def mass_convert(self):
        self.ensure_one()
        res = super().mass_convert()
        salesteam_id = self.team_id.id if self.team_id else False
        prefix_name = suffix_name = ''
        if self.prefix:
            prefix_name = self.prefix + '-'
        if self.suffix:
            suffix_name = '-' + self.suffix
        # 被勾選的商機的銷售團隊
        lead_selected = self._context.get('active_ids', [])
        for lead_id in lead_selected:
            lead = self.env['crm.lead'].browse(lead_id)
            # 將商機 name 轉成 => 前綴 + 客戶名稱 + 後綴
            lead.name = prefix_name + lead.partner_id.name + suffix_name
            # 並將 active 改為有效狀態
            lead.active = True
            lead.user_id = self.user_id.id if self.user_id else False
            # 選擇畫面所選的銷售團隊
            lead.team_id = salesteam_id
            # 階段為該所選銷售團隊的第一個階段
            stage = self.env['crm.stage'].search(
                [('team_id', '=', salesteam_id)], order='sequence', limit=1)
            lead.stage_id = stage.id
        return res
