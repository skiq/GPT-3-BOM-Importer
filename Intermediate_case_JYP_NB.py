#!/usr/bin/env python
# coding: utf-8

# In[127]:


#!/usr/bin/env python
# coding: utf-8

#importing the necessary files
import json
import jsonlines            #because GPT3 needs files in jsonlines format
import os                   #to get the env variables from the system
import openai
import pandas as pd
import octopart_check
import time
from excel_to_csv import csv_from_excel
from results import get_result_csv


# In[128]:


# Load your API key from an environment variable named as OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

# In[129]:

def get_mpns_file(xlsx_file):
    #Creating parameters for GPT3 to learn our custome DATA
    example_text = "400.0|1.0|TCAN1042HV       |SO08        |Texas instruments||-40°C bis 85°C|Mouser|595-TCAN1042HVDR|Ja|IC201||40.0|-|1.0|FSUSB42MUX|Low Power, Two port, High Speed USB2.0 Mux|-|U8|MSOP10|SMT4.0|C4, C8, C13, C17|100nF 16V 0603|CAP 100nF 16V ±20% 0603 (1608 Metric) Thickness 1mm SMD|CAPC0603(1608)100_N|LCSC|C1590|Digikey|1276-1006-1-ND|Samsung Electro-Mechanics|CL10B104KA8NNNC|4000.0|0.004341|17.364|YES|-2.0|J2, J3|C70373|Q&J CR2032 Battery Clip|C70373|LCSC|C70373|-|-|Q&J|C70373|2000.0|0.021139|42.278|YES|Supplied by tacterion7.0|10K/75V|SM0603_HD|R2, R12, R18, R19, R29, R34, R35|VISHAY|CRCW060310K0FKEA|Chip-Widerstand|Farnell|1469748.0|22.0|T1, T2|Fitted|BC33725BU|ON Semi|2.025.0|X3, X5, X6, X7, X11|Fitted|3866g.68|Vogt Verbindungstechnik|5.013.0|D2|Fitted|WP710A10SRD/D|Kingbright|1.01.0|100R 1/4W|R1206|R201|RESISTOR, European symbol|Mouser|667-ERJ-P06F1501V|Panasonic|||DickfilmwiderstÃ¤nde - SMD 0805 1.5Kohms 0.5W 1% Tol |120.0|2.0|STCK|127.001|C 100p 50V NP0 0402 5%|SMD-KONDENSATOR|C43, C44|32.21.77, Sams CL05C101JB5NNNCZQ1|14.7456 MHz|30ppm|SMD, 11.4mm x 4.35mm|TXC  9C-14.7456MAAJ-T  XTAL, 14.7456MHZ, 18PF, SMD, HC-49S|TXC|9C-14.7456MAAJ-T||1.0|Farnell|1842289|0,41167|41167.0|| 1.0|100R 1/4W|R1206|R201|RESISTOR, European symbol|Mouser|667-ERJ-P06F1501V|Panasonic|||DickfilmwiderstÃ¤nde - SMD 0805 1.5Kohms 0.5W 1% Tol |  1.0|100R 1/4W|R1206,R1100,R2122,R21|R201|, European symbol||Panasonic||| - SMD 0833 1ohms 0.1W 5% Tol |"
    # example_text = "|025|2.0|Stk||RS-422/RS-485 Interface IC Half-Duplex RS-485/RS-422-Compatible Transceiver with AutoDirection Control|PCB|MAX13487EESA+|U1, U13|Mouser|Maxim Integrated|https://www.mouser.de/ProductDetail/Maxim-Integrated/MAX13487EESA%2b?qs=sGAEpiMZZMuXae9YOZoWd9EBnNihOkMOLMC5ITnTDKk%3D |045|1.0|Stk||Crystals 32.768kHz 3pF 20ppm -40C +125C|PCB|ABS07W-32.768kHz-K-2-T|Y4|Mouser|ABRACON|https://www.mouser.de/ProductDetail/ABRACON/ABS07W-32768kHz-K-2-T?qs=gt1LBUVyoHkCHJuAeHVlqA%3D%3D |065|8.0|Stk||100uF - 25GV|PCB|865060445005|C11, C15, C16, C25, C27, C36, C38, C72|Würth Electronics||https://www.we-online.de/katalog/de/WCAP-ASLL/?sq=865060445005#865060445005 mV|TAIWAN SEMICONDUCTOR|SK56C||1.0|Farnell|1299292|124156.0|124156.0|| |40.0|Fitted|1.0|U7|FT234XD-R|FT234XD-R - DFN12|DFN-12|FTDI|FT234XD USB to BASIC UART IC, -40 to +85 degC, 12-Pin DFN, Pb-Free, Tape and Reel|FT234XD-R||Mouser|895-FT234XD-R|E00000000144 76.0|IC1|1.0|IFX1117MEV33|Spannungsregler|SOT230P700X170-4N|Infineon Technologies 1.0|U9|DS2764|DS2764BE+025 or DS2764AE+025|Li+ battery monitor I2C bus|Dallas||||75.0|90.0|| 20.0|16.0|STCK|032.062|74HC595 16P-DHVQFN16 HC-MOS SMD|A1-8, A10, A11, A14, A15, A18, A19, A21, A22|Nexperia 74HC595BQ,115 120.0|2.0|STCK|127.001|C 100p 50V NP0 0402 5\%|SMD-KONDENSATOR|C43, C44|32.21.77, Sams CL05C101JB5NNNC"
    # q_a_examples =[["|025|2.0|Stk||RS-422/RS-485 Interface IC Half-Duplex RS-485/RS-422-Compatible Transceiver with AutoDirection Control|PCB|MAX13487EESA+|U1, U13|Mouser|Maxim Integrated|https://www.mouser.de/ProductDetail/Maxim-Integrated/MAX13487EESA%2b?qs=sGAEpiMZZMuXae9YOZoWd9EBnNihOkMOLMC5ITnTDKk%3D","MAX13487EESA+"],
    #               ["|045|1.0|Stk||Crystals 32.768kHz 3pF 20ppm -40C +125C|PCB|ABS07W-32.768kHz-K-2-T|Y4|Mouser|ABRACON|https://www.mouser.de/ProductDetail/ABRACON/ABS07W-32768kHz-K-2-T?qs=gt1LBUVyoHkCHJuAeHVlqA%3D%3D","ABS07W-32.768kHz-K-2-T"],
    #               ["|065|8.0|Stk||100uF - 25GV|PCB|865060445005|C11, C15, C16, C25, C27, C36, C38, C72|Würth Electronics||https://www.we-online.de/katalog/de/WCAP-ASLL/?sq=865060445005#865060445005","865060445005"],
    #               ["D1|SK56C||SMC|Gleichrichterdiode, Miniatur, Einfach, 60 V, 5 A, DO-214AB, 2, 750 mV|TAIWAN SEMICONDUCTOR|SK56C||1.0|Farnell|1299292|124156.0|124156.0||","SK56C"],
    #               ["|40.0|Fitted|1.0|U7|FT234XD-R|FT234XD-R - DFN12|DFN-12|FTDI|FT234XD USB to BASIC UART IC, -40 to +85 degC, 12-Pin DFN, Pb-Free, Tape and Reel|FT234XD-R||Mouser|895-FT234XD-R|E00000000144","FT234XD-R"],
    #               ["76.0|IC1|1.0|IFX1117MEV33|Spannungsregler|SOT230P700X170-4N|Infineon Technologies","IFX1117MEV33"],
    #               ["1.0|U9|DS2764|DS2764BE+025 or DS2764AE+025|Li+ battery monitor I2C bus|Dallas||||75.0|90.0||","DS2764"],
    #               ["20.0|16.0|STCK|032.062|74HC595 16P-DHVQFN16 HC-MOS SMD|A1-8, A10, A11, A14, A15, A18, A19, A21, A22|Nexperia 74HC595BQ,115","74HC595BQ,115"],
    #               ["120.0|2.0|STCK|127.001|C 100p 50V NP0 0402 5%|SMD-KONDENSATOR|C43, C44|32.21.77, Sams CL05C101JB5NNNC","CL05C101JB5NNNC"]]
    q_a_examples = [["400.0|1.0|TCAN1042HV       |SO08        |Texas instruments||-40°C bis 85°C|Mouser|595-TCAN1042HVDR|Ja|IC201|","595-TCAN1042HVDR"],["7.0|10K/75V|SM0603_HD|R2-R35|VISHAY|CRCW060310K0FKEA|Chip-Widerstand|Farnell|1469748.0|","CRCW060310K0FKEA"],["22.0|T1, T2|Fitted|A59-BC33725BU|ON Semi|2.0","A59-59BC33725BU"],["25.0|X3, X5, X6, X7, X11|Fitted|3866g.68|Vogt Verbindungstechnik|5.0","Vogt 3866g.68"],["13.0|D2|Fitted|WP710A10SRD/D|Kingbright|1.0","WP710A10SRD/D"],["1.0|100R 1/4W|R1206|R201|RESISTOR, European symbol|Mouser|667-ERJ-P06F1501V|Panasonic|||DickfilmwiderstÃ¤nde - SMD 0805 1.5Kohms 0.5W 1% Tol |","667-ERJ-P06F1501V"],["120.0|2.0|STCK|127.001|C 100p 50V NP0 0402 5%|SMD-KONDENSATOR|C43, C44|32.21.77, Sams CL05C101JB5NNNC","CL05C101JB5NNNC"],["ZQ1|14.7456 MHz|30ppm|SMD, 11.4mm x 4.35mm|TXC  9C-14.7456MAAJ-T  XTAL, 14.7456MHZ, 18PF, SMD, HC-49S|TXC|9C-14.7456MAAJ-T||1.0|Farnell|1842289|0,41167|41167.0||","9C-14.7456MAAJ-T"],["1.0|100R 1/4W|R1206,R1100,R2122,R21|R201|, European symbol||Panasonic||| - SMD 0833 1ohms 0.1W 5% Tol |","?"]]
    # In[130]:


    # Step1: File converted from excel to CSV with the import command
    #Getting the uploaded xlsx file from the Upload folder
    # for filename in os.listdir("UploadedFile/"):
    #     if filename.endswith(".xlsx"):
    #         xlsx_file = "UploadedFile/"+filename
    # xlsx_file = "UploadedFile/Bill of Materials-AR403.xlsx"
    print(xlsx_file)
    text_file = csv_from_excel(xlsx_file) #hardcode it for the frontend to give the path
    print(text_file)

    # In[131]:


    # # Step2: Getting the name of the csv file
    # for filename in os.listdir("UploadedFile/"):
    #     if filename.endswith(".txt"):
    #         text_file = "UploadedFile/"+filename
    #
    # # In[132]:
    #
    #
    # print(text_file)


    # In[133]:


    #Step3 : Feeding the file to GPT3 for using as the document to extract information from

    def Upload_File_for_gpt3(text_file):

        #loading the pipe seperated pre-processed test file
        with open(text_file, 'r') as file:
            training_data = file.read()

        #Convert to GPT3 accessible file format : {"text":"...","metadata":"..."}
        format_training_data = { "text" : training_data, "metadata" : ""}

        #convert the output into jsonl
        with jsonlines.open(r'UploadedFile/TestAccuracy18-1.jsonl', 'w') as writer:
            writer.write(format_training_data)

        # create file and uploading for GPT3 to access later
        for filename in os.listdir("UploadedFile/"):
            if filename.endswith(".jsonl"):
                t_file = "UploadedFile/"+filename
        gpt_file = openai.File.create(file=open(t_file), purpose='answers')

        return gpt_file["id"]

    file_id = Upload_File_for_gpt3(text_file)
    time.sleep(10)


    # In[134]:


    print(file_id)


    # In[135]:


    # Step4: Get questions from the file and use find_index() to get the index of that question
    def get_question_from_csv(file = text_file):
        with open(file, 'r') as f:
            MyData = f.readlines()
            ques_and_index = []
            for text in MyData:
                if len(text) >= 0 :
                    index = find_index(file, text)
                    q_n_t = [text,index]
                    ques_and_index.append(q_n_t) #creating a list with 2 values, question and its index
        return ques_and_index


    # In[136]:


    #Step5: Finds the index of the question from the txt file
    def find_index(file,text_to_find):
        with open(file, 'r') as f:
            MyData = f.readlines()
            for index, row in enumerate(MyData):
                if text_to_find in row:
                    return index+1


    # In[137]:


    #Step6: GPT3 in action
    def run_gpt(ques,example_text,q_a_examples):

        if len(ques) > 20:

            response = openai.Answer.create(
            model="ada",
            question= ques,
            file=file_id,
            examples_context=example_text,
            examples=q_a_examples,
            max_tokens=20,
            stop=["\n", "<|endoftext|>"]
            )
            ##get the MPN from gpt3
            MPN = response['answers'][0]

            return MPN

        else:
            return ""


    # In[138]:


    #Step 7: Get the required MPN and index by running gpt3
    def get_MPN_and_index(example_text,q_a_examples):
        ques_and_index = get_question_from_csv()
        MPN_and_index = []
        for it in (ques_and_index):
            ques = it[0]
            print(ques)
            MPN = run_gpt(ques,example_text,q_a_examples)
            index = it[1]
            print(index)
            MPN_and_index.append([index,MPN])
            print(MPN_and_index)

        return MPN_and_index



    # In[139]:


    MPN_list = get_MPN_and_index(example_text,q_a_examples)


    # In[140]:


    # MPN_list = [[1, 'Qty.|Value|Package|Parts|Producer|Producer Number|Description|Dist'], [3, 'C0603C105K3RACTU'], [5, 'GRM188R72A104KA35D'], [7, 'MC0603B102K500CT'], [9, '0603B103J500CT'], [11, 'C1608X5R1E106M080AC'], [13, '0603B103J500CT'], [15, '#|#|'], [17, 'C9'], [19, '0603B472K500CT'], [21, 'GRM31CR71A226ME15L'], [23, 'TCJB156M025R'], [25, 'C1206C475K5P'], [27, 'C3216X7T2E224M160AA'], [29, 'CD0603_S01575'], [31, 'SMAJ18CA'], [33, '634-SI8261BAC-C-IS'], [35, 'CD4093BPWR'], [37, ''], [39, 'LMH6646MM/NOB'], [41, '926-LMZ14202HTZ/NOPB'], [43, 'LMT87LPG'], [45, 'LM3480IM3-5.0'], [47, 'LT1761ES5-BYP#TRMPBF'], [49, '_331031271520'], [51, '742792097.0'], [53, 'FDV302P'], [55, 'ERJ3GEY0R00V'], [57, 'CRCW060310K0FKEA'], [59, '2447272.0'], [61, 'CRCW060320K0FKEA'], [63, '9330712.0'], [65, 'MC0063W060318K2'], [67, 'CR0603-FX-1003ELF'], [69, 'ERJ-P03J270V'], [71, 'CRCW06035K10FKEAC'], [73, '2447233.0'], [75, '#|#|Chip-Widerstand'], [77, '#'], [79, 'MC0063W060311K'], [81, 'CRCW060339K0FKEA'], [83, 'TE'], [85, 'MCWR06X3901FTL'], [87, 'WR06X3900FTL'], [89, '3.0|1K|3223W|R32, R41, RV3|'], [91, '9330941.0'], [93, '1577628.0'], [95, '3.0|1K|3223W|RV1, RV2|Bourn'], [97, 'BZX384-C16,115'], [99, 'A6S1102H'], [101, 'TP_SMD'], [103, 'S3B-ZR_THT']]


    # In[141]:


    print(xlsx_file, MPN_list)


    # In[142]:


    download_file = get_result_csv(xlsx_file,MPN_list)


    # In[143]:


    print("File is available to download - ",download_file)


    # In[144]:


    openai.File.list()


    # In[ ]:
