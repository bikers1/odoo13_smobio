# -*- coding: utf-8 -*-
# 本模組由元植管理顧問開發與維護，未經同意不得複製與散布

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
from odoo.addons import decimal_precision as dp


class ResCompany(models.Model):
    _inherit = 'res.company'

    nhi_rate = fields.Float(string='健保局費率-雇員(%)', digits=dp.get_precision('Payroll'),default=6.17)
    nhi_host_rate = fields.Float(string='健保局費率-雇主、自營業主、自行職業(%)', digits=dp.get_precision('Payroll'),default=6.17)
    nhi_avg_f = fields.Float(string='健保局-平均眷口數(人)', digits=dp.get_precision('Payroll'),default=0.58)
    nhi2_rate = fields.Float(string='2代健保局費率(%)', digits=dp.get_precision('Payroll'),default=2.11)
    bli_rate = fields.Float(string='勞保費率-勞工保險普通事故保險費率(%)', digits=dp.get_precision('Payroll'),default=10.5)
    bli2_rate = fields.Float(string='勞保費率-就業保險費率(%)', digits=dp.get_precision('Payroll'),default=1)
    bli3_rate = fields.Float(string='勞保費率-勞工保險職業災害保險費(%)', digits=dp.get_precision('Payroll'),default=0.17)
    bli4_rate = fields.Float(string='勞保費率-勞工退休金(%)', digits=dp.get_precision('Payroll'),default=6)
    

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    bli_over_rate = fields.Float(string='自提勞保退休金率(%)')
    nhi_family = fields.Integer(string='健保投保眷屬數(不含本人)')
    host_or_not = fields.Boolean(string='勞健保身分-是否為雇主', help='若為雇主請勾選(影響勞健保計算)')
    
# 20200827 因應odoo人力資源權限架構調整
class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    bli_over_rate = fields.Float(string='自提勞保退休金率(%)')
    nhi_family = fields.Integer(string='健保投保眷屬數(不含本人)')
    host_or_not = fields.Boolean(string='勞健保身分-是否為雇主', help='若為雇主請勾選(影響勞健保計算)')    
    
    
class HrContract(models.Model):
    _inherit = 'hr.contract'
    
    nhi_amount = fields.Integer(string='健保投保薪資')
    bli_amount = fields.Integer(string='勞保投保薪資')
    bli3_amount = fields.Integer(string='勞退投保薪資')
    withholding_tax = fields.Integer(string='代扣所得稅')
    food_subsidy = fields.Integer(string='伙食津貼')
    allowance1 = fields.Integer(string='津貼1(應稅)')
    allowance2 = fields.Integer(string='津貼2(應稅)')
    allowance3 = fields.Integer(string='津貼3(應稅)')
    allowance4 = fields.Integer(string='津貼4(免稅)')
    allowance5 = fields.Integer(string='津貼5(免稅)')
    contract_info = fields.Char(string='合約備註')

    
class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    payment_mode = fields.Char(string='付款方式')
    work_day_nhi = fields.Integer(string='總工作天數-勞保',compute='_compute_days')
    work_day_wage = fields.Integer(string='總工作天數-薪資',compute='_compute_days')
    all_month_day = fields.Integer(string='總工作天數-當月',compute='_compute_days')

    @api.depends(
        'date_from','date_to',
        'contract_id.date_start','contract_id.date_end')
    def _compute_days(self):
        for record in self:
            fmt = '%Y-%m-%d'
            # 計算[總工作天數-當月]
            payslip_date_start = datetime.strptime(str(record.date_from), fmt)
            payslip_date_end = datetime.strptime(str(record.date_to), fmt)
            if payslip_date_end > payslip_date_start :
                record.all_month_day = (payslip_date_end - payslip_date_start).days + 1
            else :
                raise ValidationError('結束日期必須大於起始日期')
            if record.contract_id.date_end:
                contract_date_end = datetime.strptime(str(record.contract_id.date_end), fmt)
                # 如果合約終止時間提早結束, 則將結束日期設定為合約終止時間
                if contract_date_end < payslip_date_end:
                    payslip_date_end = contract_date_end
            # 首先撈出 contract 的日期
            if record.contract_id.date_start:
                contract_date_start = datetime.strptime(str(record.contract_id.date_start), fmt)
                # 計算[總工作天數-薪資]
                # 如果合約開始時間比較近, 則以合約時間為主
                if contract_date_start > payslip_date_start:
                    record.work_day_wage = (payslip_date_end - contract_date_start).days + 1
                else:
                    record.work_day_wage = (payslip_date_end - payslip_date_start).days + 1
                if record.work_day_wage < 1:
                    record.work_day_wage = 0
                # 計算[總工作天數-勞健保]
                # 如果合約開始時間比較近, 則以合約時間為主
                if contract_date_start > payslip_date_start:
                    record.work_day_nhi = (payslip_date_end - contract_date_start).days + 1
                else:
                    record.work_day_nhi = (payslip_date_end - payslip_date_start).days + 1
                if record.work_day_nhi < 1:
                    record.work_day_nhi = 0
                if record.work_day_nhi > 30:
                    record.work_day_nhi = 30
                if payslip_date_start.month == 2 and \
                payslip_date_end.month == 2 and \
                    record.work_day_nhi >= 28:
                    record.work_day_nhi = 30
            # 未設定 contract 日期
            else:
                record.work_day_wage = 0
                record.work_day_nhi = 0
                #raise ValidationError('請建立合約開始日期')