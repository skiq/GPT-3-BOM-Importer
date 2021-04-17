#!/usr/bin/env python
# coding: utf-8

# In[578]:


#importing the necessary files
import json
import jsonlines            #because GPT3 needs files in jsonlines format
import os                   #to get the env variables from the system
import openai 
import pandas as pd
import octopart_check
import excel_to_csv
from string import ascii_uppercase


# In[579]:


# Load your API key from an environment variable named as OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")


# In[581]:


#Creating parameters for GPT3 to learn our custome DATA
example_text = "|025|2.0|Stk||RS-422/RS-485 Interface IC Half-Duplex RS-485/RS-422-Compatible Transceiver with AutoDirection Control|PCB|MAX13487EESA+|U1, U13|Mouser|Maxim Integrated|https://www.mouser.de/ProductDetail/Maxim-Integrated/MAX13487EESA%2b?qs=sGAEpiMZZMuXae9YOZoWd9EBnNihOkMOLMC5ITnTDKk%3D |045|1.0|Stk||Crystals 32.768kHz 3pF 20ppm -40C +125C|PCB|ABS07W-32.768kHz-K-2-T|Y4|Mouser|ABRACON|https://www.mouser.de/ProductDetail/ABRACON/ABS07W-32768kHz-K-2-T?qs=gt1LBUVyoHkCHJuAeHVlqA%3D%3D |065|8.0|Stk||100uF - 25GV|PCB|865060445005|C11, C15, C16, C25, C27, C36, C38, C72|Würth Electronics||https://www.we-online.de/katalog/de/WCAP-ASLL/?sq=865060445005#865060445005 mV|TAIWAN SEMICONDUCTOR|SK56C||1.0|Farnell|1299292|124156.0|124156.0|| |40.0|Fitted|1.0|U7|FT234XD-R|FT234XD-R - DFN12|DFN-12|FTDI|FT234XD USB to BASIC UART IC, -40 to +85 degC, 12-Pin DFN, Pb-Free, Tape and Reel|FT234XD-R||Mouser|895-FT234XD-R|E00000000144 76.0|IC1|1.0|IFX1117MEV33|Spannungsregler|SOT230P700X170-4N|Infineon Technologies 1.0|U9|DS2764|DS2764BE+025 or DS2764AE+025|Li+ battery monitor I2C bus|Dallas||||75.0|90.0|| 20.0|16.0|STCK|032.062|74HC595 16P-DHVQFN16 HC-MOS SMD|A1-8, A10, A11, A14, A15, A18, A19, A21, A22|Nexperia 74HC595BQ,115 120.0|2.0|STCK|127.001|C 100p 50V NP0 0402 5\%|SMD-KONDENSATOR|C43, C44|32.21.77, Sams CL05C101JB5NNNC"
q_a_examples =[["|025|2.0|Stk||RS-422/RS-485 Interface IC Half-Duplex RS-485/RS-422-Compatible Transceiver with AutoDirection Control|PCB|MAX13487EESA+|U1, U13|Mouser|Maxim Integrated|https://www.mouser.de/ProductDetail/Maxim-Integrated/MAX13487EESA%2b?qs=sGAEpiMZZMuXae9YOZoWd9EBnNihOkMOLMC5ITnTDKk%3D","MAX13487EESA+"],
              ["|045|1.0|Stk||Crystals 32.768kHz 3pF 20ppm -40C +125C|PCB|ABS07W-32.768kHz-K-2-T|Y4|Mouser|ABRACON|https://www.mouser.de/ProductDetail/ABRACON/ABS07W-32768kHz-K-2-T?qs=gt1LBUVyoHkCHJuAeHVlqA%3D%3D","ABS07W-32.768kHz-K-2-T"],
              ["|065|8.0|Stk||100uF - 25GV|PCB|865060445005|C11, C15, C16, C25, C27, C36, C38, C72|Würth Electronics||https://www.we-online.de/katalog/de/WCAP-ASLL/?sq=865060445005#865060445005","865060445005"],
              ["D1|SK56C||SMC|Gleichrichterdiode, Miniatur, Einfach, 60 V, 5 A, DO-214AB, 2, 750 mV|TAIWAN SEMICONDUCTOR|SK56C||1.0|Farnell|1299292|124156.0|124156.0||","SK56C"],
              ["|40.0|Fitted|1.0|U7|FT234XD-R|FT234XD-R - DFN12|DFN-12|FTDI|FT234XD USB to BASIC UART IC, -40 to +85 degC, 12-Pin DFN, Pb-Free, Tape and Reel|FT234XD-R||Mouser|895-FT234XD-R|E00000000144","FT234XD-R"],
              ["76.0|IC1|1.0|IFX1117MEV33|Spannungsregler|SOT230P700X170-4N|Infineon Technologies","IFX1117MEV33"],
              ["1.0|U9|DS2764|DS2764BE+025 or DS2764AE+025|Li+ battery monitor I2C bus|Dallas||||75.0|90.0||","DS2764"],
              ["20.0|16.0|STCK|032.062|74HC595 16P-DHVQFN16 HC-MOS SMD|A1-8, A10, A11, A14, A15, A18, A19, A21, A22|Nexperia 74HC595BQ,115","74HC595BQ,115"],
              ["120.0|2.0|STCK|127.001|C 100p 50V NP0 0402 5%|SMD-KONDENSATOR|C43, C44|32.21.77, Sams CL05C101JB5NNNC","CL05C101JB5NNNC"]] 


# In[582]:


# Step1: File converted from excel to CSV with the import command


# In[583]:


# Step2: Getting the name of the csv file
for filename in os.listdir("UploadedFile/"):
    if filename.endswith(".txt"):
        text_file = "UploadedFile/"+filename


# In[595]:


#Step3 : Feeding the file to GPT3 for using as the document to extract information from

def Upload_File_for_gpt3(text_file):

    #loading the pipe seperated pre-processed test file
    with open(text_file, 'r') as file:
        training_data = file.read()

    #Convert to GPT3 accessible file format : {"text":"...","metadata":"..."}
    format_training_data = { "text" : training_data, "metadata" : ""}   

    #convert the output into jsonl
    with jsonlines.open(r'UploadedFile/format_test_data.jsonl', 'w') as writer:
        writer.write(format_training_data)

    # create file and uploading for GPT3 to access later
    for filename in os.listdir("UploadedFile/"):
        if filename.endswith(".jsonl"):
            t_file = "UploadedFile/"+filename
    gpt_file = openai.File.create(file=open(t_file), purpose='answers')
    
    return gpt_file["id"]

file_id = Upload_File_for_gpt3(text_file)


# In[585]:


# Step4: Get questions from the file and use find_index() to get the index of that question
def get_question_from_csv(file = text_file):
    with open(file, 'r') as f: 
        MyData = f.readlines()
        ques_and_index = []
        for text in MyData:
            if len(text) > 50 :
                index = find_index(file, text)
                q_n_t = [text,index]
                ques_and_index.append(q_n_t) #creating a list with 2 values, question and its index
    return ques_and_index


# In[586]:


#Step5: Finds the index of the question from the txt file
def find_index(file,text_to_find): 
    with open(file, 'r') as f: 
        MyData = f.readlines() 
        for index, row in enumerate(MyData):
            if text_to_find in row:
                return index+1


# In[596]:


#Step6: GPT3 in action
def run_gpt(ques,example_text,q_a_examples):    

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
    
    return MPN,response


# In[597]:


#Step 7: Get the required MPN and index by running gpt3
def get_MPN_and_index(example_text,q_a_examples):
    ques_and_index = get_question_from_csv()
    MPN_and_index = []
    for it in (ques_and_index):
        ques = it[0]        
        MPN,response = run_gpt(ques,example_text,q_a_examples)
        index = it[1]
        MPN_and_index.append([MPN,index])
        
    return MPN_and_index
    


# In[598]:


MPN_list = get_MPN_and_index(example_text,q_a_examples)


# In[599]:


print(MPN_list)


# In[600]:


#Checking list of uploaded files
# openai.File.list()
# openai.File.delete("file-WwlEmlKmGOjjneemTEB8ktJR")


# In[ ]:


# def validate_MPN(MPN):
#     match = demo_match_mpn(client,str(MPN))
#     return match


# In[ ]:


# def create_excel_file():
#     """can use pandas or xlsxwriter"""
#     pass
#     return new_excel_file


# In[ ]:


# def print_to_excel(match,new_excel_file):    
#     """ get the information from validator and put it in the correct row of newly created excel sheet"""
    
#     pass
#     print("File is ready to download")


# In[ ]:




