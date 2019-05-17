# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 02:17:01 2019

@author: Kyunglok Baik
"""

import matplotlib.pyplot as plt
import pandas as pd
from pandas.tools.plotting import parallel_coordinates
import numpy as np

import json
import os
import csv
import time
import process as pc
import feature_convert as fc

import scipy.interpolate as interp

#from sklearn.decomposition import PCA as sklearnPCA
#from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
#from sklearn.datasets.samples_generator import make_blobs

default_dir = 'E:/CIL_messages/'
#default_dir = '/media/ky/easystore/CIL_messages/'

#file=open(default_dir+'cil_reader_trimmed.json','r',encoding='utf-8')
#k=file.read().split('\n\n')
#kson=[json.loads(i) for i in k]
#kson_source_ip=set([kson[i]['src_ip'] for i in range(len(kson))])
#kson_tagged_src_ip = pc.tag_by_src_ip(kson)
#kson_cat = pc.sort_by_srcip_by_categories(kson)
#
#gps_inter_time=fc.s_interarrival_time_gps(kson_cat)
#voxel_inter_time=fc.s_interarrival_time_voxel_forecast(kson_cat)
#voxel_duration = fc.interarrival_time_voxel_duration(kson_cat)
#perf_inter_time = fc.s_interarrival_time_detailed_performance(kson_cat)
#
#s_gps_inter_time = fc.s_interarrival_time_gps(kson_cat)
#s_performance_inter_time = fc.s_interarrival_time_detailed_performance(kson_cat)
#s_voxel_inter_time = fc.s_interarrival_time_voxel_forecast(kson_cat)

#function input: dictionary form of {"ip_address":np.diff(list)}
# These are per round bases
def plot_graphs(dic):
    #save_path=default_dir+'plots/'+str(time.time())+'/'
    #if not os.path.exists(save_path):
        #os.makedirs(save_path)
    for key in dic:
        #file=open(save_path+key.replace('.','_')+'.csv','w',encoding='utf-8')
        #file.write(dic[key])
        #file.close()
        plt.figure()
        plt.title(str(key))
        plt.scatter(np.arange(len(dic[key]))/len(dic[key]),dic[key],alpha=0.5)
        plt.xlabel('Distribution 0 ~ 1')
        plt.ylabel('Values')
        plt.show()
        try:
            print(min(dic[key]),max(dic[key]),sum(dic[key])/len(dic[key]))
        except ValueError:
            print('oops')
     #plt.legend(dic.keys())
         #plt.savefig(save_path+(str(key).replace('.','_'))+'.png')

def plot_distribution_graphs_grouped(dic, title='', x='Distribution (0-1.0)', y='Value'):
    plt.figure(figsize=(20,10))
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    for key in dic:
        plt.plot(np.arange(len(dic[key]))/len(dic[key]), dic[key],alpha=0.65)
    plt.legend(dic.keys())
    plt.show()

def plot_all(lst_dic, title='', x='Distribution (0-1.0)', y='Value'):
    plt.figure(figsize=(20,10))
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    lstip=[]
    for i in range(len(lst_dic)):
        cnt=1
        for key in lst_dic[i]:
            if lst_dic[i][key] != []:
                plt.plot(np.arange(len(lst_dic[i][key]))/len(lst_dic[i][key]), lst_dic[i][key], c=(i%10/10,(i+1)%10/10,(i+2)%10/10),alpha=0.5+0.5/cnt)
                lstip.append(str(i)+':'+str(key))
                cnt+=1
    #all_ip = [x for xs in lstip for x in xs]
    plt.legend(lstip)
    plt.xlim((0.0,1.2))    
    print(str(len(lstip))+' instances')
    plt.show()

#def convolute(lst_dic, title='', x='Distribution (0-1.0)', y='Value'):
    