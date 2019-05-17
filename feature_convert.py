# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 02:58:46 2019

@author: Kyunglok Baik
"""

import numpy as np
import scipy.interpolate as spi

def convert_json_to_csv(i_var):
    pass

#interpolate a dic
def k_interpolate(lst,n=500):
    x2 = np.linspace(0,1.0,n)
    x=list(np.arange(len(lst))/len(lst))
    y=lst
    if  lst != []:
        ipo = spi.splrep(x,y,k=1)
        iy= spi.splev(x2,ipo)
    return iy
    
    

def ps_to_s(input_s):
    return float(input_s['seconds'])+(float(input_s['picoseconds'])/1e12)


def interarrival_time_gps(kson, interp=0, n=500):
    temp_list=[]
    for j in kson['location']:
        try:
            temp_list.append(ps_to_s(j['timestamp']))
        except KeyError:
            pass
    temp_list=list(np.diff(sorted([round(i,6) for i in temp_list])))
    if interp==1:
        temp_list = k_interpolate(temp_list,n)
    return temp_list

def interarrival_time_detailed_performance(kson, interp=0, n=500):
    temp_list=[]
    for j in kson['detailed_performance']:
        try:
            temp_list.append(ps_to_s(j['timestamp']))
        except KeyError:
            pass
    temp_list=list(np.diff(sorted([round(i,6) for i in temp_list])))
    if interp==1:
        temp_list = k_interpolate(temp_list,n)
    return temp_list

def interarrival_time_voxel_forecast(kson, interp=0, n=500):
    temp_list=[]
    for j in kson['spectrum_usage']:
        try:
            temp_list.append(ps_to_s(j['timestamp']))
        except KeyError:
            pass
    temp_list=list(np.diff(sorted([round(i,6) for i in temp_list])))
    if interp==1:
        temp_list = k_interpolate(temp_list,n)
    return temp_list


def voxel_duration(kson, interp=0, n=500):
    temp_list=[]
    for j in kson['spectrum_usage']:
        try:
            temp_list.append(ps_to_s(j['spectrum_usage']['voxels'][0]['spectrum_voxel']['time_end'])
                                -ps_to_s(j['spectrum_usage']['voxels'][0]['spectrum_voxel']['time_start']))
        except KeyError:
            #print(json.loads(j))
            #break
            pass
    if interp==1:
        temp_list = k_interpolate(temp_list,n)
    return temp_list

  