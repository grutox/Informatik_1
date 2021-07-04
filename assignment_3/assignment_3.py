######################################################################
# Author: Thomas Gruber

# Description: The main file Assignment_3
# Comments: Enter the input file (ass_2.p) and the output path
######################################################################

import argparse
import bokeh
import collections
import math
import matplotlib
import numpy
import os 
import pickle
import scipy
import seaborn
import struct
import sys
import time
import matplotlib.pyplot as plt
import numpy as np


def data_load():
    
    # instantiate a parser 
    arg_parser = argparse.ArgumentParser()
    # Add our parameters
    arg_parser.add_argument("-i", "--in", default = "ass_2.p")
    arg_parser.add_argument("-o", "--out", default = "./")
     
    cmd_params = vars(arg_parser.parse_args()) 
    path  = cmd_params["in"]
    output = cmd_params["out"]
    output_par = output.split("/")
    directory = output_par[0]
# look for the input file and output directory    
    if not os.path.isfile(path):
        print("[ERROR] Input pickle '%s' not found."%path)
        exit()
    if not os.path.isdir(directory):
        print("[ERROR] Output directory '%s' not found."%directory) 
        exit()
    return(path, output)
    
# start looking for drives with an "a"        
def combine(path,output): 
    with open(path, "rb") as input_pickle:
            dictionary = pickle.load(input_pickle)
    list_drive = []
    
    for drive in sorted(dictionary.keys()):
        list_drive.append(drive[0:8])
    counter = 0
# when an "a" is found, start the function check()    
    for drive in list_drive: 
        search_drive = drive[0:7] + "a"
        if drive == search_drive:
            found_drive = drive
            check(found_drive[0:7],counter,\
                  list_drive[counter:],dictionary,output)
        counter +=1      
    return(dictionary,output)    
            
# now look for the next drives and the correct alphabet           
def check(found_drive,counter,list_drive,dictionary,output):
    abc = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
           "n","o","p","q","r","s","t","u","v","w","x","y","z"]

    position = 0
    list_found_drive = []
    
    for drive in sorted(list_drive):
        search_drive = drive[0:7] + abc[position]
# first look for the correct number
        if drive[0:7] == found_drive:
# second look for the correct ending
            if drive == search_drive:
                list_found_drive.append(drive)
                position +=1
            else:
                print("no combination",drive)
                return("No combination possible")
            
# break if there is the next number of drives           
        else: 
            print("next drive ",drive)
            break
# list with the drives, which could be combined           
    ref_drive = list_found_drive[0]
# delete the ref_drive from the list 
    list_found_drive.pop(0)

# now compare all relevant keys with the ref drive    
    ref_num_signals = dictionary[ref_drive]["num_signals"]
    ref_frequency = dictionary[ref_drive]["frequency"]
    #ref_num_samples = dictionary[ref_drive]["num_samples"]
    ref_signals = []
    for signal in dictionary[ref_drive]["signals"].keys():
        ref_signals.append(signal)
        
    for drive in list_found_drive:
        new_num_signals = dictionary[drive]["num_signals"]
        new_frequency = dictionary[drive]["frequency"]
        #new_num_samples = dictionary[drive]["num_samples"]
        new_signals = []
        
        for signal in dictionary[drive]["signals"].keys():
            new_signals.append(signal)

        if new_frequency != ref_frequency:
            #print("frequency ist not compatible")
            return()
     
        if new_signals != ref_signals:
            #print("signals ist not compatible")
            return()
        
        if new_num_signals != ref_num_signals:
            return()
            
                   
    for drive in list_found_drive:
        for signal in ref_signals:
            ref_file_name = dictionary[ref_drive]["signals"]\
                    [signal]["file_name"]
            ref_data_format = dictionary[ref_drive]["signals"][signal]\
                    ["data_format"]
            ref_samples_per_frame = dictionary[ref_drive]["signals"]\
                    [signal]["samples_per_frame"]
            ref_unit = dictionary[ref_drive]["signals"][signal]["unit"]
            ref_adc_resolution = dictionary[ref_drive]["signals"]\
                    [signal]["adc_resolution"]
            ref_adc_zero = dictionary[ref_drive]["signals"][signal]\
                    ["adc_zero"]
            #ref_initial_value = dictionary[ref_drive]["signals"]\
                    #[signal]["initial_value"]
            #ref_check_sum = dictionary[ref_drive]["signals"]\
                    #[signal]["checksum"]
            ref_block_size = dictionary[ref_drive]["signals"]\
                    [signal]["block_size"]
            
            if not dictionary[ref_drive]["signals"][signal]["data"]:
                #print("Data in ",signal, "is empty")
                return("Data in", signal, "is empty")
            
            new_file_name = dictionary[drive]["signals"][signal]\
                    ["file_name"]
            new_data_format = dictionary[drive]["signals"][signal]\
                    ["data_format"]
            new_samples_per_frame = dictionary[drive]["signals"]\
                    [signal]["samples_per_frame"]
            new_unit = dictionary[drive]["signals"][signal]["unit"]
            new_adc_resolution = dictionary[drive]["signals"][signal]\
                    ["adc_resolution"]
            new_adc_zero = dictionary[drive]["signals"][signal]\
                    ["adc_zero"]
            #new_initial_value = dictionary[drive]["signals"]\
            #       [signal]["initial_value"]
            #new_check_sum = dictionary[drive]["signals"]\
            #       [signal]["checksum"]
            new_block_size = dictionary[drive]["signals"]\
                   [signal]["block_size"]
# compare all with the ref drive           
            if not dictionary[drive]["signals"][signal]["data"]:
                #print("Data in ",signal, "is empty")
                return("Data in", signal, "is empty")
                
            if new_data_format != ref_data_format:
                #print("wrong data format")
                return("Wrong data format")
            
            if new_samples_per_frame != ref_samples_per_frame:
                #print("wrong samples_per_frame")
                return("wrong samples_per_frame")
            
            if new_unit != ref_unit:
                #print("wrong unit")
                return("Wrong unit")
                
            if new_adc_resolution != ref_adc_resolution:
                #print("wrong adc_resolution")
                return("Wrong adc_resolution")
                
            if new_adc_zero != ref_adc_zero:
                #print("wrong adc_zero")
                return("Wrong adc_zero")
            
            if new_block_size != ref_block_size:
                #print("wrong block size")
                return("wrong block size")
                
    new_drive = ref_drive[0:-1]
 
# add new key in the dictionary 
    dictionary[new_drive] = dictionary[ref_drive]
# change the name ind "drivexy" without an "a"
    dictionary[new_drive]["record_name"] = new_drive
# now combine the drives, add the data 
    for drive in list_found_drive:
        dictionary[new_drive]["num_samples"] = dictionary[new_drive]\
                ["num_samples"] + dictionary[drive]["num_samples"]
        
        for signal in dictionary[new_drive]["signals"].keys():
# add the data to the new key in the dictionary
            dictionary[new_drive]["signals"][signal]["data"]\
                    .extend(dictionary[drive]["signals"][signal]["data"])
# change the filename to "drivexy" without an "a"
            dictionary[new_drive]["signals"][signal]["file_name"] = \
                new_drive + ".dat"
# delete other drives form the dictionary 
        del dictionary[drive]
# also delete the ref_drive
    del dictionary[ref_drive]
 
# calculate the new checksum   
    for signal in dictionary[new_drive]["signals"].keys():
        check_sum = 0
        daten = dictionary[new_drive]["signals"][signal]["data"]
        for i in daten:
            sum_tuple = sum(i)
            check_sum = check_sum + sum_tuple
        check_16bit = check_sum & 65535
        checksum = struct.unpack("h", struct.pack("H", check_16bit))[0]
        dictionary[new_drive]["signals"]["resp"]["checksum"] = checksum
        
    return(dictionary)
    
# store the new pickle_file    
def store_dictionary(dictionary,output):

    outputFile = open(output + "/ass_3.p", "wb")
    pickle.dump(dictionary, outputFile)
    outputFile.close()
      
def plot_drives(dictionary,output):
    for drive in dictionary.keys():
        no_data = False
        sensor_number = 0
# len_sensor for the subplots
        len_sensor = len(dictionary[drive]["signals"].keys())       
        
#search for data in the drive/sensor
        for sensor in dictionary[drive]["signals"].keys():
            if dictionary[drive]["signals"][sensor]["data"]:
                break
            else:
                len_sensor = len_sensor - 1
# if all "data"-keys in the drive are empty, plot nothing                 
            if len_sensor == 0:
                print("there is no data in this drive")
                no_data = True
        
        if no_data == True:
            continue
            
# create two plots for short and full_data     
        figure,axis = plt.subplots((len_sensor))
        figure_short,axis_short = plt.subplots((len_sensor))
        for sensor in dictionary[drive]["signals"].keys():
            
            if not dictionary[drive]["signals"][sensor]["data"]:
                continue
# calculate the time with the frequency and the samples_per_frame       
            samples_per_frame = dictionary[drive]["signals"]\
                    [sensor]["samples_per_frame"]
            frequency = dictionary[drive]["frequency"]
            num_samples = dictionary[drive]["num_samples"]
            data = dictionary[drive]["signals"][sensor]["data"]
            time_per_sample = (1/frequency)/samples_per_frame
            
# create a flat list with all datas            
            data_flat = np.array(dictionary[drive]["signals"]\
                                 [sensor]["data"]).flatten()


# calculate the time and create a list
            xs = []
            counter = 0
            for time in data_flat:
                xs.append(counter * time_per_sample)
                counter += 1
    
            data_short = []
            xs_short = []
            counter = 0
            
# create a list with for 45-50
            for time in xs:
                if time >= 45:
                    if time >= 50:
                        data_short.append(data_flat[counter])
                
                counter += 1
                
# calculate the new time
            time_per_sample = 5/(len(data_short))
            counter = 0
            for time in data_short:
                xs_short.append(45 + counter * time_per_sample)
                counter +=1

# if there are just in ones sensor data
# don't make supluts!
            if len_sensor == 1:
                
                axis.step(xs, data_flat)
                axis.set_ylabel(sensor+"      ",rotation = "0")
                axis.set_xlabel("Time in s")   
                axis.set_yticklabels([])
                figure.subplots_adjust(hspace=0)
                
                axis_short.step(xs_short, data_short)
                axis_short.set_ylabel(sensor+"      ",rotation = "0")
                axis_short.set_xlabel("Time in s")
                axis_short.set_yticklabels([])
                figure_short.subplots_adjust(hspace=0)
                
            if len_sensor > 1:
    
                axis[sensor_number].step(xs, data_flat)
                axis[sensor_number].set_ylabel(sensor+"       ",\
                            rotation = "0")
                axis[len_sensor-1].set_xlabel("Time in s")
                axis[sensor_number].set_yticklabels([])
                figure.subplots_adjust(hspace=0)
                
                axis_short[sensor_number].step(xs_short, data_short)
                axis_short[sensor_number].set_ylabel(sensor+"      ",\
                             rotation = "0")
                axis_short[len_sensor-1].set_xlabel("Time in s")
                axis_short[sensor_number].set_yticklabels([])
                figure_short.subplots_adjust(hspace=0)
            
            sensor_number += 1
            
            
# store the plots in the output path          
        figure.savefig(output+"/"+"%s_full.png"%drive, 
               transparent=False,
               bbox_inches="tight")
        figure.savefig(output+"/"+"%s_full.pdf"%drive, 
               transparent=False, 
               bbox_inches="tight")
    
        figure_short.savefig(output+"/"+"%s_short.png"%drive, 
               transparent=False,
               bbox_inches="tight")
        figure_short.savefig(output+"/"+"%s_short.pdf"%drive, 
               transparent=False, 
               bbox_inches="tight")
        
        plt.close('all')
        
      
if __name__ == "__main__":
    
    path, output  = data_load()

    dictionary,output = combine(path,output)
    
    store_dictionary(dictionary,output)
    
    plot_drives(dictionary,output)
    
