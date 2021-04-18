import xlrd
import csv
import os

"""
input: sheet
return: index of header

identify header

for line in sheet:
if number of populated cells is max AND it's the first line with this count
we assume this is the header
"""
def get_header_line_index(sh):
    # store in array
    row_number_filled = []

    # for each line, check number of populated cells
    for row in range(sh.nrows):
        filled = 0

        for column in range(sh.ncols):
            if not (sh.cell_value(row,column)==''):
                filled+=1

        row_number_filled.append(filled)

    max_width = max(row_number_filled)

    # return first index you can find that is equal to max width
    for i in range(len(row_number_filled)):
        if row_number_filled[i] == max_width:
            return i

"""
input: Excel file

output: index of the line that it thinks is the header
"""
def get_header_line_index_from_xls(file):
    wb = xlrd.open_workbook(file)
    sh = wb.sheet_by_index(0)
    index = get_header_line_index(sh)
    return index

"""
convert excel workbook to pipe-separated txt file
drop all lines up until header row (disabled)

Note:
- saves file to same folder as input file
- retains same name, just replaces extension with "txt"
"""
def csv_from_excel(file, sheet_index = 0, header_row = 0):
    wb = xlrd.open_workbook(file)
    sh = wb.sheet_by_index(sheet_index)
    your_csv_file = open(file.split('.xls')[0] + ".txt", 'w')
    wr = csv.writer(your_csv_file, delimiter='|', encoding='utf-8') #, quoting=csv.QUOTE_ALL

    # max_width = sh.computed_column_width()
    for rownum in range(sh.nrows):
        # if rownum >= header_row:
        #     wr.writerow(sh.row_values(rownum))
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

# convert all files in any given folder from Excel to our csv format
if __name__ == '__main__':
    bom = '/Users/swenkoller/Desktop/GPT3 Makeathon/Code/data/Bill of Materials-D-Muster_Pyramid _V1(Standard).xlsx'

    header_index = get_header_line_index_from_xls(bom)

    csv_from_excel(bom,header_row = header_index)


    # for filename in os.listdir("data/"):
    #     if filename.endswith(".xls") or filename.endswith(".xlsx"):
    #         csv_from_excel("data/" + filename, index = 0)
    #         print("converting " + filename)
    #         continue
    #     else:
    #         continue
