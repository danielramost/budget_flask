import xlsxwriter

from datetime import datetime

def excel_from_matrix(file_name, data):
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    date_format = workbook.add_format()
    date_format.set_num_format('dd/mm/yyyy')

    for row in range(len(data)):
        for col in range(len(data[row])):
            if type(data[row][col]) is datetime:
                worksheet.write(row, col, data[row][col], date_format)
            else:
                worksheet.write(row, col, data[row][col])

    workbook.close()
