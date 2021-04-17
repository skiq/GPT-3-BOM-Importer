# get input Excel
# get index
# get attributes
# build new excel with all data
import xlrd
import csv
from octopart_check import match_single_mpn

"""
takes as input a list of octopart results and indices
"""
# def get_solution_table(indices, octopart_output_list):



"""
# Input: array excel_indices, mpn_candidates
# return: % of lines with valid MPN candidates

input:
[[0,None],
[1,FCA234234NL],
[2,FLACA2334NL],
…. ]
"""
def number_of_mpns(mpn_candidates):
    counter = 0
    for i in mpn_candidates:
        if len(i) > 1:
            counter+=1
    return counter

def mpn_blank_ratio(mpn_candidates):
    return number_of_mpns(mpn_candidates) / len(mpn_candidates)

def valid_mpn_ratio(mpn_candidates):
    valid = 0
    for row in mpn_candidates:
        if len(row) > 1:
            if match_single_mpn(row[1]) != None:
                valid+=1

    total = number_of_mpns(mpn_candidates)
    return valid / total

"""
# input: original excel file + array excel_indices, mpn_candidates
# return: ;-delimited csv file with concatenated MPN to the right

removes invalid mpns
"""
def append_excel_with_mpns_get_csv(original_excel,mpn_candidates):

    remove_invalid_mpns(mpn_candidates)

    wb = xlrd.open_workbook(original_excel)
    sh = wb.sheet_by_index(0)
    your_csv_file = open(original_excel.split('.xls')[0] + ".txt", 'w')
    wr = csv.writer(your_csv_file, delimiter=';') #, quoting=csv.QUOTE_ALL

    # max_width = sh.computed_column_width()
    for rownum in range(sh.nrows):
        # if rownum >= header_row:
        #     wr.writerow(sh.row_values(rownum))
        if len(mpn_candidates[rownum]) > 1:
            cell_values = sh.row_values(rownum)
            cell_values.append(mpn_candidates[rownum][1])
            print(cell_values)
            wr.writerow(cell_values)
        else:
            wr.writerow(sh.row_values(rownum))

    your_csv_file.close()
    return new_excel_file

"""
takes list as input and deletes all invalid MPNs
"""
def remove_invalid_mpns(mpn_candidates):
    for candidate in mpn_candidates:
        if len(candidate) > 1:
            if match_single_mpn(candidate[1]) is None:
                del candidate[1]
        else:
            continue

# count = get_number_of_mpns([[0],
# [1,"FCA234234NL"],
# [2,"FLACA2334NL"]])
if __name__ == '__main__':
    mpns = [[0],
            [1,"FCA234234NL"],
            [2,"FLACA2334NL"],
            [3,"LMC6482IMX/NOPB"]]
    original_excel_file = '/Users/swenkoller/Desktop/GPT3 Makeathon/Code/data/Bill of Materials-D-Muster_Pyramid _V1(Standard).xlsx'
    append_excel_with_mpns_get_csv(original_excel_file,mpns)
    # count = get_number_of_mpns([[0],
    # [1,"FCA234234NL"],
    # [2,"FLACA2334NL"]])
    # print(count)
