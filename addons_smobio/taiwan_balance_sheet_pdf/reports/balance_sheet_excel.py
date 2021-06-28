# -*- coding: utf-8 -*-
from odoo import api, fields, models


class BalanceSheetExcel(models.AbstractModel):
    _name = 'report.taiwan_balance_sheet_pdf.balance_sheet_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self,workbook, data, objects):
        format1 = workbook.add_format({'font_size': 11, 'align': 'vcenter', 'text_wrap': 1, 'bold': True, 'top': 1, 'left': 1, 'right': 1,'bottom': 1})  # 設定EXCEL儲存格式, 字體11, 垂直置中, 自動換行(text_wrap), 粗體,  上下左右邊框1px
        format1.set_align('center')  # 設定EXCEL儲存格式, 水平置中
        format2 = workbook.add_format({'font_size': 11, 'align': 'vcenter', 'text_wrap': 1, 'bold': True, 'top': 1, 'left': 1, 'right': 1,'bottom': 1})
        format2.set_align('left')  # 設定EXCEL儲存格式, 向左對齊
        format3 = workbook.add_format({'font_size': 11, 'align': 'vcenter', 'text_wrap': 1, 'bold': True, 'top': 1, 'left': 1, 'right': 1, 'bottom': 1})
        format3.set_align('right')  # 設定EXCEL儲存格式, 向右對齊
        format3.set_num_format(3)

        i = 0
        sheet = workbook.add_worksheet('TWBS 台灣會計報表-資產負債表')  # 建立EXCEL工作頁籤
        sheet.set_column('A:A', 60)
        sheet.set_column('B:B', 20)
        sheet.merge_range(0, 0, 0, 1, 'TWBS 台灣會計報表-資產負債表', format1)
        i += 1
        sheet.merge_range(i, 0, i, 1, '期間: %s ~ %s' % (data.get('date_from'), data.get('date_to')), format2)
        i += 1
        sheet.write(i, 0, '科目名稱', format1)
        sheet.write(i, 1, '金額', format1)
        i += 1

        for line in data.get('report_lines'):
            if line['level'] != 0:
                sheet.write(i, 0, '%s%s' % ('  ' * int(line.get('level', 0)), line.get('name')), format2)
                if line.get('name') != '' and line.get('account_type') != 'sum':
                    sheet.write(i, 1, line.get('balance'), format3)
                elif line.get('name') == '' or line.get('account_type') == 'sum':
                    sheet.write(i, 1, '', format3)
                else:
                    sheet.write(i, 1, '', format3)
            else:
                sheet.write(i, 0, '', format1)
                sheet.write(i, 1, '', format1)
            i += 1
