# -*- coding: utf-8 -*-
from odoo import api, fields, models


class TaiwanBalanceSheetExcel(models.AbstractModel):
    _name = 'report.taiwan_balance_sheet_pdf.taiwan_balance_sheet_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self,workbook, data, objects):
        format1 = workbook.add_format({'font_size': 11, 'align': 'vcenter', 'text_wrap': 1, 'bold': True, 'top': 1, 'left': 1, 'right': 1,'bottom': 1})  # 設定EXCEL儲存格式, 字體11, 垂直置中, 自動換行(text_wrap), 粗體,  上下左右邊框1px
        format1.set_align('center')  # 設定EXCEL儲存格式, 水平置中
        format2 = workbook.add_format({'font_size': 11, 'align': 'vcenter', 'text_wrap': 1, 'bold': True, 'top': 1, 'left': 1, 'right': 1,'bottom': 1})
        format2.set_align('left')  # 設定EXCEL儲存格式, 向左對齊
        format3 = workbook.add_format({'font_size': 11, 'align': 'vcenter', 'text_wrap': 1, 'bold': True, 'top': 1, 'left': 1, 'right': 1, 'bottom': 1})
        format3.set_align('right')  # 設定EXCEL儲存格式, 向右對齊
        format3.set_num_format(3)

        report_lines = data.get('report_lines')
        left_lines, right_lines = report_lines.get('left_lines'), report_lines.get('right_lines')

        date_from, date_to = data.get('date_from') if data.get('date_from') else '', data.get('date_to') if data.get('date_to') else ''

        i = 0
        sheet = workbook.add_worksheet('TWBS 台灣會計報表-資產負債表')  # 建立EXCEL工作頁籤
        sheet.set_column('A:A', 40)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 40)
        sheet.set_column('D:D', 15)
        sheet.merge_range(0, 0, 0, 3, 'TWBS 台灣會計報表-資產負債表', format1)
        i += 1
        sheet.merge_range(i, 0, i, 3, '期間: %s ~ %s' % (date_from, date_to), format3)
        i += 1
        sheet.write(i, 0, '科目名稱', format1)
        sheet.write(i, 1, '金額', format1)
        sheet.write(i, 2, '科目名稱', format1)
        sheet.write(i, 3, '金額', format1)
        i += 1
        j = 0
        for line in left_lines:
            if line['level'] != 0:
                sheet.write(i, 0, '%s%s' % ('  ' * int(line.get('level', 0)), line.get('name')), format2)
                if line.get('name') != '' and line.get('account_type') != 'sum':
                    sheet.write(i, 1, line.get('balance'), format3)
                elif line.get('name') == '' or line.get('account_type') == 'sum':
                    sheet.write(i, 1, '', format3)
                else:
                    sheet.write(i, 1, '', format3)

                sheet.write(i, 2, '%s%s' % ('  ' * int(right_lines[j].get('level', 0)), right_lines[j].get('name')), format2)
                if right_lines[j].get('name') != '' and right_lines[j].get('account_type') != 'sum':
                    sheet.write(i, 3, right_lines[j].get('balance'), format3)
                elif right_lines[j].get('name') == '' and right_lines[j].get('account_type') == 'sum':
                    sheet.write(i, 3, '', format3)
                else:
                    sheet.write(i, 3, '', format3)
            else:
                sheet.write(i, 0, '', format1)
                sheet.write(i, 1, '', format1)
                sheet.write(i, 2, '', format1)
                sheet.write(i, 3, '', format1)
            j += 1
            i += 1
