# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountReportExcel(models.AbstractModel):
    _name = 'report.accounting_pdf_reports.account_report_xlsx'
    _inherit = 'report.odoo_report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        format1 = workbook.add_format({'font_size': 11, 'align': 'vcenter', 'text_wrap': 1, 'bold': True, 'top': 1, 'left': 1, 'right': 1,'bottom': 1})  # 設定EXCEL儲存格式, 字體11, 垂直置中, 自動換行(text_wrap), 粗體,  上下左右邊框1px
        format1.set_align('center')  # 設定EXCEL儲存格式, 水平置中
        format2 = workbook.add_format({'font_size': 11, 'align': 'vcenter', 'text_wrap': 1, 'bold': True, 'top': 1, 'left': 1, 'right': 1,'bottom': 1})
        format2.set_align('left')  # 設定EXCEL儲存格式, 向左對齊
        format3 = workbook.add_format({'font_size': 11, 'align': 'vcenter', 'text_wrap': 1, 'bold': True, 'top': 1, 'left': 1, 'right': 1, 'bottom': 1})
        format3.set_align('right')  # 設定EXCEL儲存格式, 向右對齊
        format3.set_num_format(3)
        cash_sheet, debit_credit, enable_filter = data.get('cash_sheet'), data.get('debit_credit'), data.get('enable_filter')
        date_from, date_to = data.get('date_from') if data.get('date_from') else '', data.get('date_to') if data.get('date_to') else ''

        i, j = 0, 0
        sheet = workbook.add_worksheet(data.get('report_type_name'))  # 建立EXCEL工作頁籤

        if debit_credit:
            sheet.set_column('A:A', 30)
            sheet.set_column('B:E', 20)
            j = 1
        else:
            sheet.set_column('A:A', 30)
            sheet.set_column('B:D', 20)
        sheet.merge_range(0, 0, 0, 3 + j, data.get('report_type_name'), format1)
        i += 1
        sheet.merge_range(i, 0, i, 1, '分錄種類: %s' % ('All Entries' if data.get('target_move') == 'all' else 'All Posted Entries'), format2)
        sheet.merge_range(i, 2, i, 3 + j, '期間: %s ~ %s' % (date_from, date_to),  format2)
        i += 1

        if debit_credit == 1:
            sheet.write(i, 0, '科目名稱', format1)
            if cash_sheet:
                sheet.write(i, 1, '期初金額', format1)
            else:
                sheet.write(i, 1, '', format1)
            sheet.write(i, 2, '借方', format1)
            sheet.write(i, 2, '貸方', format1)
            sheet.write(i, 3, '餘額', format1)
            i += 1

            for line in data.get('report_lines'):
                if line['level'] != 0:
                    sheet.write(i, 0, '%s%s' % ('  ' * int(line.get('level', 0)), line.get('name')), format2)
                    if cash_sheet and line.get('type') == 'account' and line.get('initial_balance') != 0:
                        sheet.write(i, 1, line.get('initial_balance'), format3)
                    else:
                        sheet.write(i, 1, '', format3)
                    sheet.write(i, 2, line.get('debit'), format3)
                    sheet.write(i, 3, line.get('credit'), format3)
                    sheet.write(i, 4, line.get('balance'), format3)
                i += 1
        elif not enable_filter and not debit_credit:
            sheet.write(i, 0, '科目名稱', format1)
            if cash_sheet:
                sheet.write(i, 1, '期初金額', format1)
            else:
                sheet.write(i, 1, '', format1)
            sheet.merge_range(i, 2, i, 3, '餘額', format1)
            i += 1

            for line in data.get('report_lines'):
                if line['level'] != 0:
                    sheet.write(i, 0, '%s%s' % ('  ' * int(line.get('level', 0)), line.get('name')), format2)
                    print(line.get('type'), line.get('initial_balance'))
                    if cash_sheet and line.get('type') == 'account' and line.get('initial_balance') != 0:
                        sheet.write(i, 1, line.get('initial_balance'), format3)
                    else:
                        sheet.write(i, 1, '', format3)
                    sheet.merge_range(i, 2, i, 3, line.get('balance'), format3)
                i += 1
        elif enable_filter and not debit_credit:
            sheet.write(i, 0, '科目名稱', format1)
            if cash_sheet:
                sheet.write(i, 1, '期初金額', format1)
            else:
                sheet.write(i, 1, '', format1)
            sheet.write(i, 2, '餘額', format1)
            i += 1
            sheet.write(i, 3, 'label_filter', format1)
            i += 1

            for line in data.get('report_lines'):
                if line['level'] != 0:
                    sheet.write(i, 0, '%s%s' % ('  ' * int(line.get('level', 0)), line.get('name')), format2)
                    if cash_sheet and line.get('type') == 'account' and line.get('initial_balance') != 0:
                        sheet.write(i, 1, line.get('initial_balance'), format3)
                    else:
                        sheet.write(i, 1, '', format3)
                    sheet.write(i, 2, line.get('balance'), format3)
                    sheet.write(i, 3, line.get('balance_cmp'), format3)
                i += 1
