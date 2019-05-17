# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 09:46:20 2019

@author: Kyunglok Baik
"""

default_dir = 'E:/CIL_messages/'
#default_dir = '/media/ky/easystore/CIL_messages/'
cil_reader_dir = 'E:/cil_reader_data/'
cil_checker_dir = 'E:/cil_checker_data/'

import json
import numpy as np
import feature_convert as fc
from os import listdir
from os.path import isfile, join
import sys

file=open(default_dir+'cil_reader_trimmed.json','r',encoding='utf-8')
k=file.read().split('\n\n')
kson=[json.loads(i) for i in k]
kson_source_ip=set([kson[i]['src_ip'] for i in range(len(kson))])

#create a list of source ip, destination ip and record time stamp for occurrances
def tag_source_to_dst(list_json):
    lst=[]
    final_dic={}
    for i in list_json:
        ipset = str(i['src_ip'])+'->'+str(i['dst_ip'])
        if ipset not in lst:
            final_dic[ipset] = [i]
            lst.append(ipset)
            
        else:
            final_dic[ipset] = final_dic[ipset] + [i]
            
    return final_dic

# sorts messages containing features by source ip address
def tag_by_src_ip(list_json):
    list_ip=list(set([list_json[i]['src_ip'] for i in range(len(list_json))]))
    message_sets_by_ip = {}
    for i in list_ip:
        message_sets_by_ip[i] = [j for j in list_json if j['src_ip'] == i]
    return message_sets_by_ip
    

# this is to see if all the keys in each json file match
def json_key_checker(list_json):
    lst_keys=[]
    for i in list_json:
        if i.keys() not in lst_keys:
            lst_keys.append(list(i.keys()))
    return lst_keys

def cilmessage_key_checker(list_json):
    lst_keys=[]
    for i in list_json:
        if i['cil_message'].keys() not in lst_keys:
            lst_keys.append(i['cil_message'].keys())
    return lst_keys


def convert_type(val):
    if type(val) is str:
        return val.encode()
    elif type(val) is int:
        return float(val)
    return val
        

#kson_tagged_src_ip = tag_by_src_ip(kson)
#kson_tagged_src_to_dst = tag_source_to_dst(kson)

def get_location_by_ip(list_json):
    log = ""
    location = []
    for i in range(0,len(list_json)):
        boo = True
        try:
            t = list_json[i]['cil_message']['location_update']['locations']['location']
            latitude=t['latitude']
            longitude=t['longitude']
            location.append({'coordinate': {'latitude': latitude,'longitude':longitude}, 'ip_src_to_dst': (i['src_ip'], i['dst_ip'])})
        except (TypeError, KeyError):
            boo=False
        finally:
            log += '%r a location message: %d th message\n' % (boo,i) 
    return {'log':log, 'locations':location}

def classify_message(list_json):
    k=tag_by_src_ip(list_json)
    tdic={}
    #for individual IP
    for i in k:
        message=[]
        #for individual messages in each IP
        for j in k[i]:
            temp=j['cil_message']
            if 'hello' in temp:
                message.append((j['timestamp'],1))
            elif 'location_update' in temp:
                message.append((j['timestamp'],2))
            elif 'detailed_performance' in temp:
                message.append((j['timestamp'],3))
            elif 'spectrum_usage'  in temp:
                message.append((j['timestamp'],4))
            elif 'incumbent_notify' in temp:
                message.append((j['timestamp'],5))
            else:
                message.append((j['timestamp'],6))
        tdic[i] = message
    return tdic

def moving_window_maker(classified_message_by_ip, size=5):
    windows=[]
    for i in classified_message_by_ip:
        sub_windows=[]
        for j in range(len(classified_message_by_ip[i])-size):
            sub_windows.append(np.array(list(classified_message_by_ip[i][j:j+size])))
        windows.append(sub_windows)
    return windows


#sort by ip, and to subcateogires of each payloads
def sort_by_srcip_by_categories(list_json):
    k=tag_by_src_ip(list_json)
    for i in k:
        tdic={'hello':[],'location':[],'detailed_performance':[],
                      'spectrum_usage':[],'incumbent':[],'cnt':0}
        hello=[]
        location=[]
        detailed_performance=[]
        spectrum_usage=[]
        incumbent=[]
        rest=[]
        cnt=0
        for j in k[i]:
            temp=j['cil_message']
            if 'hello' in temp:
                hello.append(temp)
                cnt+=1
            elif 'location_update' in temp:
                location.append(temp)
                cnt+=1
            elif 'detailed_performance' in temp:
                detailed_performance.append(temp)
                cnt+=1
            elif 'spectrum_usage'  in temp:
                spectrum_usage.append(temp)
                cnt+=1
            elif 'incumbent_notify' in temp:
                incumbent.append(temp)
                cnt+=1
            else:
                rest.append(temp)
                cnt+=1
        tdic['hello'] = hello
        tdic['location'] = location
        tdic['detailed_performance'] = detailed_performance
        tdic['spectrum_usage'] = spectrum_usage
        tdic['incumbent'] = incumbent
        tdic['else'] = rest
        tdic['cnt']=cnt
        k[i] = tdic
    return k


kson_cat = sort_by_srcip_by_categories(kson)

onlyfiles = [f for f in listdir(cil_reader_dir) 
                if isfile(join(cil_reader_dir, f))]
#onlyfiles = [f for f in listdir('E:/cil_reader_data/') 
#                if isfile(join('E:/cil_reader_data/', f))]

onlyfiles_pe2 = [f for f in listdir(cil_reader_dir+'pe2/') 
                if isfile(join(cil_reader_dir+'pe2/', f))]
#onlyfiles_pe2 = [f for f in listdir('E:/cil_reader_data/pe2/') 
#                if isfile(join('E:/cil_reader_data/pe2/', f))]

import random
pe2_20 = random.sample(onlyfiles_pe2, 20)

def opener(names):
    full_list=[]
    for k in names:
        file=open(cil_reader_dir+ k, 'r', encoding='utf-8')
        lst = [json.loads(i) for i in file.read().split('\n\n') if i.strip() != '']
        full_list.append(sort_by_srcip_by_categories(lst))
    return full_list

def opener_scrimmage2(names):
    full_list=[]
    for k in names:
        file=open(cil_reader_dir+ k, 'r', encoding='utf-8')
        lst = [json.loads(i) for i in file.read().split('\n\n') if i.strip() != '']
        full_list.append(sort_by_srcip_by_categories(lst))
    return full_list


def cvt_moving_windows(dic, windowsize=10):
    dic_windows={}
    for i in dic:
        lst_windows=[]
        for j in range(len(dic[i])-windowsize):
            lst_windows.append(np.array(dic[i][j:j+windowsize]))
        dic_windows[i] = lst_windows
    return dic_windows



def opener_pe2_gps(names):
    full_list=[]
    for k in names:
        file=open(cil_reader_dir+ k, 'r', encoding='utf-8')
        if sys.getsizeof(file) != 0:
            try:
                lst = [json.loads(i) for i in file.read().split('\n\n') if i.strip() != '']
                full_list.append(fc.interarrival_time_gps(sort_by_srcip_by_categories(lst),1,500))
            except KeyError:
                pass
    return full_list

def opener_pe2_dp(names):
    full_list=[]
    for k in names:
        file=open(cil_reader_dir+ k, 'r', encoding='utf-8')
        if sys.getsizeof(file) != 0:
            try:
                lst = [json.loads(i) for i in file.read().split('\n\n') if i.strip() != '']
                full_list.append(fc.interarrival_time_detailed_performance(sort_by_srcip_by_categories(lst),1,500))
            except KeyError:
                pass
    return full_list

def opener_pe2_voxel(names):
    full_list=[]
    for k in names:
        file=open(cil_reader_dir+'pe2/'+ k, 'r', encoding='utf-8')
        if sys.getsizeof(file) != 0:
            try:
                lst = [json.loads(i) for i in file.read().split('\n\n') if i.strip() != '']
                full_list.append(fc.interarrival_time_voxel_forecast(sort_by_srcip_by_categories(lst),1,500))
            except KeyError:
                pass
    return full_list
    
def opener_sc2_gps(names):
    full_list=[]
    for k in names:
        file=open(cil_reader_dir+'scrimmage2/'+ k, 'r', encoding='utf-8')
        if sys.getsizeof(file) != 0:
            try:
                lst = [json.loads(i) for i in file.read().split('\n\n') if i.strip() != '']
                full_list.append(fc.interarrival_time_gps(sort_by_srcip_by_categories(lst),1,500))
            except KeyError:
                pass
    return full_list

def opener_sc2_dp(names):
    full_list=[]
    for k in names:
        file=open(cil_reader_dir+'scrimmage2/'+ k, 'r', encoding='utf-8')
        if sys.getsizeof(file) != 0:
            try:
                lst = [json.loads(i) for i in file.read().split('\n\n') if i.strip() != '']
                full_list.append(fc.interarrival_time_detailed_performance(sort_by_srcip_by_categories(lst),1,500))
            except KeyError:
                pass
    return full_list

def opener_sc2_voxel(names):
    full_list=[]
    for k in names:
        file=open(cil_reader_dir+'scrimmage2/'+ k, 'r', encoding='utf-8')
        if sys.getsizeof(file) != 0:
            try:
                lst = [json.loads(i) for i in file.read().split('\n\n') if i.strip() != '']
                full_list.append(fc.interarrival_time_voxel_forecast(sort_by_srcip_by_categories(lst),1,500))
            except KeyError:
                pass
    return full_list

    
#k_all = opener(onlyfiles)

def cvt_opener_data(opened):
    x=[]
    y=[]
    for i in opened:
       for key in i:
           x.append(np.array(i[key]))
           y.append(key)
    return (np.stack(x),np.array(y))

def tag_dic_by_key(dic):
    data=[]
    target=[]
    for i in dic:
        for t in dic[i]:
            data.append(t)
            target.append(i)
    return (data,target)
