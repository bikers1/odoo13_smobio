# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AccountingReport(models.TransientModel):
    _inherit = "accounting.report"
    _description = "Taiwan Balance Sheet"

    type = fields.Selection(selection=[('1', '報告式PDF'), ('2', '帳戶式PDF'), ('3', '報告式EXCEL'), ('4', '帳戶式EXCEL')], string='報表類型', default='2')

    def check_report(self):
        res = super(AccountingReport, self).check_report()
        data = {}
        data['form'] = self.read(['account_report_id', 'date_from_cmp', 'date_to_cmp', 'journal_ids', 'filter_cmp', 'target_move', 'type'])[0]
        for field in ['account_report_id']:
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]
        comparison_context = self._build_comparison_context(data)
        res['data']['form']['comparison_context'] = comparison_context
        return res

    def _print_report(self, data):
        data['form'].update(self.read(['date_from_cmp', 'debit_credit', 'date_to_cmp', 'filter_cmp', 'account_report_id', 'enable_filter', 'label_filter', 'target_move', 'type'])[0])
        res_id = self.env['ir.model.data'].sudo().search([('name', '=', 'taiwan_balance_sheet')]).res_id
        if data['form']['account_report_id'][0] == res_id and data['form']['type'] == '2':
            return self.env.ref('taiwan_balance_sheet_pdf.action_report_financial_tw').report_action(self, data=data, config=False)
        else:
            return self.env.ref('accounting_pdf_reports.action_report_financial').report_action(self, data=data, config=False)

    def taiwan_balance_sheet_excel(self):
        res = self.check_report()
        if self.type == '3':
            report_lines = self.env['report.accounting_pdf_reports.report_financial'].get_account_lines(res['data']['form'])
            return {'type': 'ir.actions.report',
                    'report_name': 'taiwan_balance_sheet_pdf.balance_sheet_xlsx',
                    'report_type': "xlsx",
                    'data': {'report_lines': report_lines, 'date_from': self.date_from, 'date_to': self.date_to}}
        if self.type == '4':
            report_lines = self.env['report.taiwan_balance_sheet_pdf.report_financial_tw'].get_account_lines(res['data']['form'])
            report_lines = self.env['report.taiwan_balance_sheet_pdf.report_financial_tw'].taiwan_balance_sheet_data(report_lines)
            return {'type': 'ir.actions.report',
                    'report_name': 'taiwan_balance_sheet_pdf.taiwan_balance_sheet_xlsx',
                    'report_type': "xlsx",
                    'data': {'report_lines': report_lines, 'date_from': self.date_from, 'date_to': self.date_to}}
