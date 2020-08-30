import xlsxwriter

def excel_from_matrix(file_name, data):
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    for row in range(len(data)):
        for col in range(len(data[row])):
            worksheet.write(row, col, data[row][col])

    workbook.close()
