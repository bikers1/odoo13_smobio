# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from odoo.exceptions import UserError, ValidationError


class ResPartner2OpportunityMassConvert(models.TransientModel):

    _name = 'res.partner2opportunity.partner.mass'

    prefix = fields.Char(string='商機名稱前綴')
    suffix = fields.Char(string='商機名稱後綴')
    partner_ids = fields.Many2many('res.partner', string='Contacts')
    user_id = fields.Many2one('res.users', 'Salesperson', index=True)
    team_id = fields.Many2one(
        'crm.team', 'Sales Channel', oldname='section_id', index=True)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_ids = self.env.context.get('active_ids')
        if self.env.context.get('active_model') == 'res.partner' and active_ids:
            res['partner_ids'] = active_ids
        return res

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
        salesteam_id = self.team_id.id if self.team_id else False
        # 被勾選的 res.partner
        partner_selected = self._context.get('active_ids', [])
        prefix_name = suffix_name = ''
        if self.prefix:
            prefix_name = self.prefix + '-'
        if self.suffix:
            suffix_name = '-' + self.suffix
        res = dict()
        for partner_id in partner_selected:
            partner = self.env['res.partner'].browse(partner_id)
            # 將商機 name 轉成 => 前綴 + 客戶名稱 + 後綴
            name = prefix_name + partner.name + suffix_name
            lead = self.env['crm.lead'].create({'name': name})
            lead.partner_id = partner.id
            lead.email_from = partner.email
            lead.phone = partner.phone
            # 並將 active 改為有效狀態
            lead.active = True
            lead.user_id = self.user_id.id if self.user_id else False
            # 設定 type
            lead.type = 'opportunity'
            # 選擇畫面所選的銷售團隊
            lead.team_id = salesteam_id
            # 階段為該所選銷售團隊的第一個階段
            stage = self.env['crm.stage'].search(
                [('team_id', '=', salesteam_id)], order='sequence', limit=1)
            lead.stage_id = stage.id
        return res
