######################################################################
# Author: Thomas Gruber
# MatNr: 1625378
# Description: The main file Assignment_2 
# Comments: Enter the input file (ass_1.p) and the outputfile (ass_2.p)
#           to verify the check_sum enter --verify, and for the Pearson 
#           Correlation Coefficient enter --gsr
######################################################################

import argparse, collections, math, os, pickle, scipy, struct, sys
from scipy.stats import pearsonr

def main():
   
# instantiate a parser 
    arg_parser = argparse.ArgumentParser()
# Add our parameters
    arg_parser.add_argument("-i", "--in", default = "ass_1.p")
    arg_parser.add_argument("-o", "--out", default = "ass_2.p")
    arg_parser.add_argument("-d", "--data", default = "DATA/")
    arg_parser.add_argument("--verify", action = "store_true")
    arg_parser.add_argument("--gsr", action = "store_true")
    

    cmd_params = vars(arg_parser.parse_args()) 
    values = []
    for i in cmd_params.values():
        values.append(i)
 
    data = []
    for i in values[2]:
        data.append(i)
    if not data[-1] == "/":
        data.append("/")
        
#input File    
    file = values[0]
    
#path zum File
    path = values[2]
    
#output pickle
    path_out = values[1]                           


# exit the program if the file doesn`t exist                            
    if not os.path.exists(file):
        print("File does not exist")
        exit() 

# load the pickle file and save the dictionary
    dictionary = pickle.load(open(values[0],"rb"))

# add the key data for each signal
    for drive in dictionary.keys():
        for sensor in dictionary[drive]["signals"].keys():
            dictionary[drive]["signals"][sensor]["data"]=[]  
    
# fill the dictionary with the data from the .bin file
    for drive in dictionary.keys():
        sorted (dictionary[drive]["signals"])
        found_data = os.path.isfile(path + drive + ".dat")
        
# if the file does`t exist, continue with the next file
        if found_data == 0:
            continue          
        
        files = open (path + drive + ".dat","rb")
        counter = 1
        while counter <= dictionary[drive]["num_samples"]: 
            for si in dictionary[drive]["signals"].keys():
                signal = dictionary[drive]["signals"][si]
                data = (files.read(signal["samples_per_frame"]*2))
                data=struct.unpack(signal["samples_per_frame"]*"h",data)
                dictionary[drive]["signals"][si]["data"].append(data)
            counter = counter + 1
        files.close


# store the dictionary as pickle file  
    outputFile = open(path_out, "wb")
    pickle.dump(dictionary, outputFile)
    outputFile.close()
    
# verify Data if, the Parameter verify = true  
    if cmd_params["verify"] == 1:
        verify(dictionary,path)
        
# calculate de Coefficient if the Parameter gsr = true
    if cmd_params["gsr"] == 1:
        korrelation(dictionary,path)
        
# function to verify the data
def verify(dictionary,path):
    for drive in dictionary.keys():
        found_data = os.path.isfile(path + drive + ".dat")
        
        if found_data == 0:
            continue
        
# calculate the checksum for each sensor       
        for sensor in dictionary[drive]["signals"].keys():
            check_sum = 0
            daten = dictionary[drive]["signals"][sensor]["data"]
            for i in daten:
                sum_tuple = sum(i)
                check_sum = check_sum + sum_tuple
            check = dictionary[drive]["signals"][sensor]["checksum"]
            
            
# 65535 = 16 bit in binär with logical AND
            check_16bit = check_sum & 65535    
                       
            if check < 0:
                check_16bit = check_sum % 65536
                check_16bit = check_sum % 32768
                check_16bit = -32768 + check_16bit 

            if not check_16bit == check:
                print("CHECKSUM FAILED ", drive,sensor)
                

#function for the Pearson Correlation coefficient        
def korrelation(dictionary, path):

# search for the files with hand_gsr & foot_gsr
    drives = []
    for drive in dictionary.keys():
        found_data = os.path.isfile(path + drive + ".dat")
        
        if found_data == 0:
            continue
        
        foot_gsr = 0
        hand_gsr = 0
        for sensor in dictionary[drive]["signals"].keys():
            
# check for foot_gsr
            if sensor == "foot gsr":
                foot_gsr = 1
                
# check for hand_gsr
            if sensor == "hand gsr":
                hand_gsr = 1
                
# safe this files in th list drives      
        if foot_gsr ==1 & hand_gsr == 1:
            drives.append(drive)
# calculate the average of each frame
    for drive in drives:
        average = 0
        average_list_foot = []
        average_list_hand = []
        daten = dictionary[drive]["signals"]["foot gsr"]["data"]
        s_p_f = "samples_per_frame"
        si = "signals"
        for i in daten:
            sum_tuple = sum(i)
            average = sum_tuple/dictionary[drive][si]["foot gsr"][s_p_f]
            average_list_foot.append(average)
        daten = dictionary[drive]["signals"]["hand gsr"]["data"]
        for i in daten:
            sum_tuple = sum(i)
            average = sum_tuple/dictionary[drive][si]["hand gsr"][s_p_f]
            average_list_hand.append(average)
        
# calculate the pearson correlation coefficient       
        pea = scipy.stats.pearsonr(average_list_foot, average_list_hand)
        pea = round(pea[0],4)
        print("GSR", drive, pea)
                
# main function        
if __name__ == "__main__":
    main()
    
    
    