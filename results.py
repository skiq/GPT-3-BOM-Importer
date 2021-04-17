import xlrd
import csv
from octopart_check import match_single_mpn


"""
How to use

from results import get_result_csv

get_result_csv('FILE.xls',MPN_LIST)

"""



"""
takes as input a list of octopart results and indices
"""

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

def valid_mpns(mpn_candidates):
    valid = 0
    for row in mpn_candidates:
        if len(row) > 1:
            if match_single_mpn(row[1]) != None:
                valid+=1
    return valid

def valid_mpn_ratio_overall(mpn_candidates):
    valid = valid_mpns(mpn_candidates)
    lines = len(mpn_candidates)
    return valid / lines


def valid_mpn_ratio(mpn_candidates):
    valid = valid_mpns(mpn_candidates)
    total_candidates = number_of_mpns(mpn_candidates)
    return valid / total_candidates

"""
# input: original excel file + array excel_indices, mpn_candidates
# return: ;-delimited csv file with concatenated MPN to the right

removes invalid mpns
"""
def append_excel_with_mpns_get_csv(original_excel,mpn_candidates):

    wb = xlrd.open_workbook(original_excel)
    sh = wb.sheet_by_index(0)
    your_csv_file = open(original_excel.split('.xls')[0] + ".csv", 'w')
    wr = csv.writer(your_csv_file, delimiter=',', quoting=csv.QUOTE_ALL)

    # max_width = sh.computed_column_width()
    for rownum in range(sh.nrows):
        # if rownum >= header_row:
        #     wr.writerow(sh.row_values(rownum))
        if len(mpn_candidates[rownum]) > 1:
            cell_values = sh.row_values(rownum)
            cell_values.append(mpn_candidates[rownum][1])
            # print(cell_values)
            wr.writerow(cell_values)
        else:
            wr.writerow(sh.row_values(rownum))

    your_csv_file.close()
    return

def get_result_csv(original_excel_file,mpns):
    remove_invalid_mpns(mpns)
    append_excel_with_mpns_get_csv(original_excel_file,mpns)
    return original_excel_file.split(".xls")[0] + ".csv"

"""
takes list as input and deletes all invalid MPNs
"""

def remove_invalid_mpns_with_octopart(mpn_candidates):
    index = 0

    for candidate in mpn_candidates:
        index=+1
        if len(candidate) > 1:
            match = match_single_mpn(candidate[1])
            if match is None:
                del candidate[1]
        else:
            continue

def garbage_string(mpn_string):
    if len(mpn_string) < 5:
        return True
    else:
        return False

def remove_invalid_mpns_other(mpn_candidates):
    index = 0

    for candidate in mpn_candidates:
        index=+1
        if len(candidate) > 1:
            if garbage_string(candidate[1]):
                del candidate[1]
        else:
            continue

def remove_invalid_mpns(mpn_candidates):
    remove_invalid_mpns_other(mpn_candidates)
    remove_invalid_mpns_with_octopart(mpn_candidates)


if __name__ == '__main__':
    mpns = [[1, 'Qty.|Value|Package|Parts|Producer|Producer Number|Description|Dist'], [3, 'C0603C105K3RACTU'], [5, 'GRM188R72A104KA35D'], [7, 'MC0603B102K500CT'], [9, '0603B103J500CT'], [11, 'C1608X5R1E106M080AC'], [13, '0603B103J500CT'], [15, '#|#|'], [17, 'C9'], [19, '0603B472K500CT'], [21, 'GRM31CR71A226ME15L'], [23, ''], [25, 'C1206C475K5P'], [27, 'C3216X7T2E224M160AA'], [29, 'CD0603_S01575'], [31, 'SMAJ18CA'], [33, '634-SI8261BAC-C-IS'], [35, 'CD4093BPWR'], [37, ''], [39, 'LMH6646MM/NOB'], [41, '926-LMZ14202HTZ/NOPB'], [43, 'LMT87LPG'], [45, 'LM3480IM3-5.0'], [47, 'LT1761ES5-BYP#TRMPBF'], [49, '_331031271520'], [51, '742792097.0'], [53, 'FDV302P'], [55, 'ERJ3GEY0R00V'], [57, 'CRCW060310K0FKEA'], [59, '2447272.0'], [61, 'CRCW060320K0FKEA'], [63, '9330712.0'], [65, 'MC0063W060318K2'], [67, 'CR0603-FX-1003ELF'], [69, 'ERJ-P03J270V'], [71, 'CRCW06035K10FKEAC'], [73, '2447233.0'], [75, '#|#|Chip-Widerstand'], [77, '#'], [79, 'MC0063W060311K'], [81, 'CRCW060339K0FKEA'], [83, 'TE'], [85, 'MCWR06X3901FTL'], [87, 'WR06X3900FTL'], [89, '3.0|1K|3223W|R32, R41, RV3|'], [91, '9330941.0'], [93, '1577628.0'], [95, '3.0|1K|3223W|RV1, RV2|Bourn'], [97, 'BZX384-C16,115'], [99, 'A6S1102H'], [101, 'TP_SMD'], [103, 'S3B-ZR_THT']]


    # remove_invalid_mpns(mpns)
    #
    original_excel_file = '/Users/swenkoller/Desktop/GPT3 Makeathon/Code/data/24.01.2019_GZ 4136 1200b _(_vi_BOM_CSV_Komma).xlsx'
    # append_excel_with_mpns_get_csv(original_excel_file,mpns)

    print(get_result_csv(original_excel_file,mpns))


    # print("mpn_blank_ratio")
    # print(mpn_blank_ratio(mpns))
    #
    # print("valid_mpn_ratio")
    # print(valid_mpn_ratio(mpns))
    #
    # print("valid_mpn_ratio_overall")
    # print(valid_mpn_ratio_overall(mpns))

    # mpns = [[0],
    #         [1,"FCA234234NL"],
    #         [2,"FLACA2334NL"],
    #         [3,"LMC6482IMX/NOPB"]]
    # count = get_number_of_mpns([[0],
    # [1,"FCA234234NL"],
    # [2,"FLACA2334NL"]])
    # print(count)
