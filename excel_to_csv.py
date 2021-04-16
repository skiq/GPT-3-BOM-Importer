import xlrd
import csv
import os

# def widest_row():


def csv_from_excel(file, index):
    wb = xlrd.open_workbook(file)
    sh = wb.sheet_by_index(0)
    your_csv_file = open(file.split('.xls')[0] + ".txt", 'w')
    wr = csv.writer(your_csv_file, delimiter='|') #, quoting=csv.QUOTE_ALL

    # max_width = sh.computed_column_width()
    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

# runs the csv_from_excel function:
# csv_from_excel('PiCM_F_16BOM.xlsx', index = 0)

for filename in os.listdir("data/"):
    if filename.endswith(".xls") or filename.endswith(".xlsx"):
        csv_from_excel("data/" + filename, index = 0)
        print("converting " + filename)
        continue
    else:
        continue
