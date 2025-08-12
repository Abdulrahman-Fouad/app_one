from ast import literal_eval

from odoo import http
from odoo.http import request
import io
import xlsxwriter


class XlsxPropertyReport(http.Controller):
    @http.route("/property/excel/report/<string:property_ids>", type="http", auth="user")
    def download_property_excel_report(self, property_ids):
        property_ids = literal_eval(property_ids)
        property_records = request.env['property'].browse(property_ids)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Properties')

        header_format = workbook.add_format({'bold': True,'bg_color': '#D3D3D3','border': 1,'align': 'center'})
        string_format = workbook.add_format({'align': 'center','border': 1})
        price_format = workbook.add_format({'align': 'center', 'border': 1, 'num_format': '$##,##00.00',})

        headers = ['Name', 'Postcode', 'Selling Price', 'Garden']

        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)

        for row_num, property_record in enumerate(property_records):
            worksheet.write(row_num + 1, 0, property_record.name, string_format)
            worksheet.write(row_num + 1, 1, property_record.postcode, string_format)
            worksheet.write(row_num + 1, 2, property_record.selling_price, price_format)
            worksheet.write(row_num + 1, 3, 'Yes' if property_record.garden else 'No', string_format)

        workbook.close()
        output.seek(0)
        file_name = 'Property Report.xlsx'

        return request.make_response(output.getvalue(), headers=[
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            ('Content-Disposition', f'attachment; filename = {file_name}')
        ])
