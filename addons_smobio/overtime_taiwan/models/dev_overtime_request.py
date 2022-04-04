# -*- coding: utf-8 -*-
#
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class dev_overtime_request(models.Model):
    _name = 'dev.overtime.request'
    _inherit = 'mail.thread'
    _order='name desc'
    
    name = fields.Char('Name', default='/', copy=False)
    employee_id = fields.Many2one('hr.employee','Employee',required="1")
    date = fields.Date('Request Date', required="1", copy=False, default=fields.Date.context_today)
    hour = fields.Float('Hour', required="1",copy=False)
    confirm_date = fields.Date('Confirm Date',)
    comfirm_manager = fields.Many2one('res.users','Confirm Manager',track_visibility='onchange')
    dept_id = fields.Many2one('hr.department','Department')
    manager_id = fields.Many2one('hr.employee','Department Manager',required="1")

    user_id = fields.Many2one('res.users','User',default=lambda self: self.env.user,copy=False)
    state= fields.Selection([('draft','Draft'),('request','Waiting For Manager Approval'),('approval','Waiting For HR Confirm'),('hr_confirm','HR Confirmed'),('reject','Rejected'),('done','Done'),('cancel','Cancel')], string='State', default='draft',track_visibility='onchange')

    per_hour_amount = fields.Float('Hourly Wages')
    reason = fields.Text('Reason', required=True)
    payslip_id = fields.Many2one('hr.payslip','Payslip', copy=False)

    pay_1_33_hours = fields.Float('1.33倍加班工時')
    pay_1_67_hours = fields.Float('1.67倍加班工時')
    pay_2_hours = fields.Float('2倍加班工時')
    check_meno = fields.Text('加班查核備註')

    attendance_ids = fields.Many2many("hr.attendance", string="出勤紀錄")
    holidays_id = fields.Many2one('hr.leave.allocation', '補休分配紀錄')

    # @api.multi
    def loaded_attendance(self):
        self.ensure_one()
        attendance_ids = self.env['hr.attendance'].search([
            ('employee_id', '=', self.employee_id.id),
        ])
        # 檢查 Request Date
        if self.date:
            # 取出加班單的需求日期
            request_date = fields.Datetime.from_string(self.date).date()
            attendances_meet_request_date = []
            for attendance_id in attendance_ids:
                # 取出出勤紀錄的日期
                # 上班日期
                check_in_date = fields.Datetime.from_string(
                    attendance_id.check_in).date()
                # 下班日期
                check_out_date = fields.Datetime.from_string(
                    attendance_id.check_out).date()
                if request_date == check_in_date or request_date == check_out_date:
                    attendances_meet_request_date.append(attendance_id.id)
            # print(attendances_meet_request_date)
            self.attendance_ids = attendances_meet_request_date

    def set_to_hr_confirm(self):
        self.state = 'hr_confirm'

    # @api.multi
    def holidays_arrange(self):
        self.ensure_one()
        form_id = self.env.ref('hr_holidays.hr_leave_allocation_view_form_manager')
        overtime_name = '%s-%s-補休' % (self.name, self.date.strftime('%Y-%m-%d'))
        compensatory_leave_id = self.employee_id.company_id.compensatory_leave_id

        return {
            'type': 'ir.actions.act_window',
            'name': '休假分配',
            'res_model': 'hr.leave.allocation',
            # 'domain': [('id', 'in', finally_request_ids)],
            'context': {
                'default_type': 'add',
                'default_name': overtime_name,
                'default_holiday_status_id': compensatory_leave_id.id,
                'default_number_of_hours_display': self.hour,
                'default_notes': self.reason,
                'default_employee_id': self.employee_id.id,
                'default_holiday_type': 'employee',
                'default_overtime_request_id': self.id,
                'default_number_of_days': self.hour / 8,
            },
            'view_id': form_id.id,
            # 'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }

    @api.onchange('hour', 'pay_1_33_hours', 'pay_1_67_hours', 'pay_2_hours')
    def onchange_partner_id_warning(self):
        warning = {}
        title = "確認訊息"
        message = "加班工時超過員工申請加班時數，確認無誤請點選【OK】按鈕"
        warning = {
            'title': title,
            'message': message,
        }

        total_hours = self.pay_1_33_hours + self.pay_1_67_hours + self.pay_2_hours
        if self.hour < total_hours:
            return {'warning': warning}
        return {'domain': {}}


    @api.onchange('employee_id')
    def onchage_emp(self):
        if self.employee_id:
            self.dept_id = self.employee_id.department_id and self.employee_id.department_id.id or False
            self.manager_id = self.employee_id.parent_id and self.employee_id.parent_id.id or False


    # @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        default['name'] = '/'
        return super(dev_overtime_request, self).copy(default=default)


    # @api.multi
    def unlink(self):
        for obj in self:
            if obj.state != 'draft':
                raise ValidationError(_('Request Delete in Draft State !!!'))

        return super(dev_overtime_request,self).unlink()
                
    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'dev.overtime.request') or '/'
        return super(dev_overtime_request, self).create(vals)

    # @api.multi
    def _make_url(self,model='dev.overtime.request'):
        base_url = self.env['ir.config_parameter'].get_param('web.base.url', default='http://localhost:8069')
        if base_url:
            base_url += '/web/login?db=%s&login=%s&key=%s#id=%s&model=%s' % (self._cr.dbname, '', '',self.id, model)
        return base_url

    def overtime_request(self):
        if self.hour <= 0:
            raise ValidationError('Hour must be greater then 0.')
        mail_mail = self.env['mail.mail']
        partner_pool = self.env['res.partner']

        partner_ids=[]
        if self.manager_id:
            manager_part_id = self.manager_id and self.manager_id.user_id and self.manager_id.user_id.partner_id.id
            if manager_part_id:
                if manager_part_id not in partner_ids:
                    partner_ids.append(manager_part_id)
        subject  =  self.employee_id.name + '-' + 'Overtime Request'
        if partner_ids:
            url = self._make_url()
            for partner in partner_pool.browse(partner_ids):
                if partner.email:
                    body = '''
                        Dear ''' " <b>%s</b>," % (partner.name) + '''
                        <p></p>
                        <p> Overtime '''"<b>%s</b>" % self.name +''' Request of Employee '''"<b>%s</b>" %self.employee_id.name +''' require your Approval.</p>
                        <p></p>
                        <p><b>Reason:</b> '''"%s" % self.reason+'''</p>
                        <p></p>
                        <p>Please action it accordingly</p>
                        <p> </p>
                        <p>You can access Overtime Request  from  below url </p>
                        <p>''' "%s" % url +''' </p>

                        <p>Regards, </p>
                        <p>''' "<b>%s</b>" % self.env.user.name +''' </p>
                        '''
                    mail_values = {
                        'email_from': self.env.user.partner_id.email,
                        'email_to': partner.email,
                        'subject': subject,
                        'body_html': body,
                        'state': 'outgoing',
                        # 'type': 'email',
                    }
                    mail_id = mail_mail.create(mail_values)
                    mail_id.send(True)
        self.state = 'request'
        return True

    def reject_salary_request(self):
        mail_mail = self.env['mail.mail']
        subject  =  'Overtime Request is reject'
        partner= self.user_id.partner_id
        if partner:
            url = self._make_url()
            if partner.email:
                body = '''
                    Dear ''' " <b>%s</b>," % (partner.name) + '''
                    <p></p>
                    <p> Your Overtime Request ''' "<b>%s</b>" % self.name + ''' is Reject.</p>
                    <p></p>
                    <p>Please action it accordingly</p>
                    <p> </p>
                    <p>You can access Overtime Request  from  below url </p>
                    <p>''' "%s" % url +''' </p>

                    <p>Regards, </p>
                    <p>''' "<b>%s</b>" % self.env.user.name +''' </p>
                    '''
                mail_values = {
                    'email_from': self.env.user.partner_id.email,
                    'email_to': partner.email,
                    'subject': subject,
                    'body_html': body,
                    'state': 'outgoing',
                    # 'type': 'email',
                }
                mail_id = mail_mail.create(mail_values)
                mail_id.send(True)
        self.state = 'reject'
        return True

    def set_to_draft(self):
        self.state = 'draft'

    def set_to_cancel(self):
        self.state = 'cancel'

    def set_to_done(self):
        self.state = 'done'

    def approve_request(self):
        mail_mail = self.env['mail.mail']
        group_id = self.env['ir.model.data'].get_object_reference('om_hr_payroll', 'group_hr_payroll_manager')[1]
        group_ids = self.env['res.groups'].browse(group_id)
        partner_pool = self.env['res.partner']
        partner_ids=[]
        for user in group_ids.users:
            partner_ids.append(user.partner_id.id)
        subject  =  self.employee_id.name + '-' + 'Overtime Request Confirmation'
        if partner_ids:
            url = self._make_url()
            for partner in partner_pool.browse(partner_ids):
                if partner.email:
                    body = '''
                        Dear ''' " <b>%s</b>," % (partner.name) + '''
                        <p></p>
                        <p> Overtime '''"<b>%s</b>" % self.name +''' Request of Employee '''"<b>%s</b>" %self.employee_id.name +'''  require your Confirmation.</p>
                        <p></p>
                        <p><b>Reason:</b> '''"%s" % self.reason+'''</p>
                        <p></p>
                        <p>Please action it accordingly</p>
                        <p> </p>
                        <p>You can access Overtime Request  from  below url </p>
                        <p>''' "%s" % url +''' </p>

                        <p>Regards, </p>
                        <p>''' "<b>%s</b>" % self.env.user.name +''' </p>
                        '''
                    mail_values = {
                        'email_from': self.env.user.partner_id.email,
                        'email_to': partner.email,
                        'subject': subject,
                        'body_html': body,
                        'state': 'outgoing',
                        # 'type': 'email',
                    }
                    mail_id = mail_mail.create(mail_values)
                    mail_id.send(True)
        self.state = 'approval'
        return True

    def confirm_request(self):
        import datetime
        mail_mail = self.env['mail.mail']
        partner_id = False
        if self.employee_id:
            if self.employee_id.user_id and self.employee_id.user_id.partner_id:
                partner_id = self.employee_id.user_id.partner_id or False
        subject  =  self.employee_id.name + '-' + 'Overtime Request Confirm'
        if partner_id:
            url = self._make_url()
            if partner_id.email:
                body = '''
                    Dear ''' " <b>%s</b>," % (partner_id.name) + '''
                    <p></p>
                    <p> Your Overtime Request ''' "<b>%s</b>" % self.name + ''' is confirmed.</p>
                    <p></p>
                    <p>Please action it accordingly</p>
                    <p> </p>
                    <p>You can access Overtime Request  from  below url </p>
                    <p>''' "%s" % url +''' </p>

                    <p>Regards, </p>
                    <p>''' "<b>%s</b>" % self.env.user.name +''' </p>
                    '''
                mail_values = {
                    'email_from': self.env.user.partner_id.email,
                    'email_to': partner_id.email,
                    'subject': subject,
                    'body_html': body,
                    'state': 'outgoing',
                    # 'type': 'email',
                }
                mail_id = mail_mail.create(mail_values)
                mail_id.send(True)
        self.state = 'hr_confirm'

        self.confirm_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.comfirm_manager = self.env.user.id
        return True


class hr_leave_allocation(models.Model):
    _inherit = 'hr.leave.allocation'

    overtime_to_allocate_leave = fields.Float(string='加班轉補休', default=0)
    overtime_request_id = fields.Many2one('dev.overtime.request')

    @api.onchange('employee_id')
    def _onchange_employee(self):
        self.manager_id = self.employee_id and self.employee_id.parent_id
        # if self.employee_id.user_id != self.env.user and self._origin.employee_id != self.employee_id:
        #     self.holiday_status_id = False
        if self.holiday_type == 'employee':
            self.department_id = self.employee_id.department_id

    @api.model
    def create(self, values):
        res_id = super(hr_leave_allocation, self).create(values)
        if res_id.number_of_hours_display == 0 and res_id.overtime_to_allocate_leave:
            res_id.number_of_hours_display = res_id.overtime_to_allocate_leave

        if res_id.overtime_request_id:
            overtime_request_id = self.env['dev.overtime.request'].search([('id', '=', res_id.overtime_request_id.id)], limit=1)
            overtime_request_id.holidays_id = res_id.id
        return res_id


class hr_payslip(models.Model):
    _inherit = 'hr.payslip'

    overtime_req_ids = fields.Many2many("dev.overtime.request",string="Ovetime Requests")
    overtime_amt = fields.Float(compute='get_overtime_amount', string='Overtime Wages',store=True)
    pay_1_33_hours = fields.Float(
        string='1.33倍加班工時合計', compute='_compute_total', store=True)
    pay_1_67_hours = fields.Float(
        string='1.67倍加班工時合計', compute='_compute_total', store=True)
    pay_2_hours = fields.Float(
        string='2倍加班工時合計', compute='_compute_total', store=True)
    overtime_request_count = fields.Integer(
        string='加班申請紀錄', compute='_compute_overtime_request_count', )

    def _compute_overtime_request_records_by_region(self, record=None):
        request_ids = []
        finally_request_ids = []
        # the record is hr.payslip model
        if record and record.employee_id:
            request_ids = self.env['dev.overtime.request'].search(
                [('employee_id', '=', record.employee_id.id),
                    ('state', '=', 'done'),
                    ('payslip_id', '=', False)])
            # 取出加班單的需求日期
            date_from = fields.Datetime.from_string(record.date_from).date()
            date_to = fields.Datetime.from_string(record.date_to).date()
            for request_id in request_ids:
                request_date = fields.Datetime.from_string(
                    request_id.date).date()
                if request_date >= date_from and request_date <= date_to:
                    # 搜集該期間的加班紀錄 id
                    finally_request_ids.append(request_id.id)
        return finally_request_ids

    # 指定要計算的欄位
    @api.depends(
        'employee_id',
        'date_from',
        'date_to',
        'overtime_req_ids.pay_1_33_hours',
        'overtime_req_ids.pay_1_67_hours',
        'overtime_req_ids.pay_2_hours')
    def _compute_total(self):
        for record in self:
            request_ids = self._compute_overtime_request_records_by_region(
                record)
            # 設定預設值為 0
            record.pay_1_33_hours = 0
            record.pay_1_67_hours = 0
            record.pay_2_hours = 0
            overtime_reqs = self.env['dev.overtime.request'].browse(
                request_ids)
            # print(request_ids)
            for overtime_req in overtime_reqs:
                record.pay_1_33_hours += overtime_req.pay_1_33_hours
                record.pay_1_67_hours += overtime_req.pay_1_67_hours
                record.pay_2_hours += overtime_req.pay_2_hours

    def _compute_overtime_request_count(self):
        self.ensure_one()
        request_ids = self._compute_overtime_request_records_by_region(self)
        self.overtime_request_count = len(request_ids)

    def overtime_request_list(self):
        self.ensure_one()
        finally_request_ids = self._compute_overtime_request_records_by_region(
            self)
        return {
            'type': 'ir.actions.act_window',
            'name': '%s~%s' % (self.date_from.strftime('%Y-%m-%d') if self.date_from else '', self.date_to.strftime('%Y-%m-%d') if self.date_to else ''),
            'res_model': 'dev.overtime.request',
            'domain': [('id', 'in', finally_request_ids)],
            # 'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def compute_total(self):
        self._compute_total()

    @api.depends('overtime_req_ids')
    def get_overtime_amount(self):
        for payslip in self:
            amount = 0
            if payslip.overtime_req_ids:
                for overtime in self.overtime_req_ids:
                    amount += overtime.hour * overtime.per_hour_amount

            payslip.overtime_amt = amount



    # @api.multi
    def action_payslip_done(self):
        res=super(hr_payslip,self).action_payslip_done()
        if self.overtime_req_ids:
            for overtime in self.overtime_req_ids:
                overtime.payslip_id = self.ids[0]

    @api.onchange('employee_id')
    def onchange_employee(self):
        if self.employee_id:
            request_ids= self.env['dev.overtime.request'].search([('employee_id','=',self.employee_id.id),('state','=','done'),('payslip_id','=',False)]).ids
            if request_ids:
                self.overtime_req_ids = [(6,0,request_ids)]


class res_company(models.Model):
    _inherit = 'res.company'

    compensatory_leave_id = fields.Many2one(
        'hr.leave.type', string='補休休假類型')



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

    
        
