######################################################################
# Author: Thomas Gruber
# MatNr: 1625378
# Description: The main file Assignment_1 only has 1 file. 
# Comments: Enter DATA/RECORDS for running the file!
######################################################################


import sys
import os
import pickle
import collections

file = "RECORDS"
path = "DATA"
    
if len(sys.argv) == 2:
    file_ = sys.argv[1]
    file_ = file_.split("/")
    file = file_[1]
    path = file_[0]
    
if path != "DATA":
    print("File does not exist. Please enter DATA/RECORDS")
    exit()
if file != "RECORDS":  
    print("File does not exist. Please enter DATA/RECORDS")
    exit()
        
files = open (path + "/" + file, "r")
records=[]
real_records=[]
for line in files:
    text = line.strip()
    records.append(text)
    data=line.strip()
    s_data=data+".hea"   
    x=os.path.isfile(path + "/" + s_data)
    if x == 1:
        print("Record: %s ... OK"%data)
        real_records.append(data)    
    else:
        print("Record: %s ... NOT FOUND - skipping"%data)
        
    
files.close()
dictionary_data = dict([])
signals = dict([])

for i in real_records:
    data = i + ".hea"    
    files = open (path + "/" + data,"r")
    read_data=[]
    
    for line in files:
        text = line.strip()
        words = text.split(" ")
        read_data.append(words)
 

    head_data = read_data[0]
    head_data[0] = head_data[0].lower()
    record_name = head_data[0]    
    read_data.remove(read_data[0])    
    dictionary_header = {"num_samples": head_data[3], 
                         "num_signals": head_data[2],
                         "record_name": head_data[0], 
                         "frequency": head_data[2]}

    for line in read_data:
        if "" in line:
            break
        
        list_words = line
        list_words[8] = list_words[8].lower()
        
        if len(list_words) > 9:
            list_words[8] = list_words[8] + " " + list_words[9]
            list_words[8] = list_words[8].lower()
            list_words.remove(list_words[9])
  
        sensor_name = list_words[8] 
        dictionary_signals = {"adc_resolution": list_words[3], 
                              "adc_zero": 0, 
                              "blcok_size": 0, 
                              "checksum": list_words[6], 
                              "data_format": list_words[1], 
                              "file_name": list_words[0],
                              "initial_value": list_words[5], 
                              "samples_per_frame":1,
                              "unit":list_words[2],
                              "sensor_name":sensor_name}
        
        signals[sensor_name] = dictionary_signals
     
        
    
    dictionary_header["signals"] = signals
    dictionary_data[record_name] = dictionary_header
    files.close()
    #dictionary does not work for the FOR
    #only the last dirve-data is in de dictionary 





