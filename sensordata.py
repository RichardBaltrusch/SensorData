# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 15:39:32 2019

@author: richardvinb
Initial evaluation: 7.81
Final evaluation: 9.70
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def smoothing(read_file):
    """ smoothes noisy data by using rolling averages"""
    firstsum = 0
    smoothingfactor = 10
    newlist = []
    for i in range(smoothingfactor):
        firstsum += read_file[i]

    newlist.append(firstsum/smoothingfactor)
    for i in range(len(read_file)-smoothingfactor):
        newlist.append((firstsum - read_file[i] + read_file[i+smoothingfactor])/smoothingfactor)
    return newlist

def main():
    """ main function"""
    file = "sensordata.csv"
    read_file = pd.read_csv(file)
    #print(type(read_file))
    #print(read_file)
    #plt.plot([x for x in range(len(read_file))], read_file["AX"])
    #plt.plot([x for x in range(len(read_file))], read_file["AY"])
    #plt.plot([x for x in range(len(read_file))], read_file["AZ"])
    read_file["Asum"] = abs(read_file["AX"]) + abs(read_file["AY"]) + abs(read_file["AZ"])
    newlist = list(read_file["Asum"])
    for i in range(2):
        newlist = smoothing(newlist)
    #raw data
    plt.plot([x for x in range(len(read_file["Asum"]))], read_file["Asum"])
    plt.show()

    #smoothed data
    #plt.plot([x for x in range(len(newlist))], newlist)
    newerlist = list(map(lambda x: abs(x-sum(newlist)/len(newlist)), newlist))
    plt.plot([x for x in range(len(newlist))], newerlist)
    plt.show()

    fftlist = np.fft.fft(newerlist)
    #fftlist = np.fft.ifft(list(map(lambda x: abs(x*100), fftlist[50:-1])))
    fftlist = np.fft.ifft(fftlist[700:-1])
    fftlist = list(map(lambda x: abs(x*100), fftlist))
    fftlist = list(map(lambda x: x-2, fftlist))
    fftlist = list(filter(lambda x: x > 0, fftlist))
    plt.plot([x for x in range(len(fftlist))], fftlist)
    plt.show()

main()
