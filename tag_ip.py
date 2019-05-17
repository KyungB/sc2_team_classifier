#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 14:40:49 2019

@author: ky
"""

import json
import numpy as np
import feature_convert as fc
from os import listdir
from os.path import isfile, join

dir_path = '/media/ky/easystore'
#dir_path = 'E:/'

onlyfiles_scrimmage2 = [f for f in listdir(dir_path+'/cil_reader_data/scrimmage2/') 
                if isfile(join(dir_path+'/cil_reader_data/scrimmage2/', f))]
checker_scrimmage2 = [f for f in listdir(dir_path+'/cil_checker_data/scrimmage2/') 
                if isfile(join(dir_path+'/cil_checker_data/scrimmage2/', f))]

valid_files = [i for i in onlyfiles_scrimmage2 if i in checker_scrimmage2]

# Recieves opened file as input
def get_ip(checker_file, path=dir_path+'/cil_checker_data/scrimmage2_fixed/'):
    return json.load(checker_file)[0]['sender_ip_address']


def trim_cil_checker_data(file, path = dir_path+'cil_checker_data/scrimmage2/', save_path = dir_path+'cil_checker_data/scrimmage2_fixed/'):
    f = open(path+file,'r')
    lines = f.readlines()
    f.close()
    res = []
    for l in lines:
        if 'ERROR' not in l:
            res.append(l)
    fs = open(save_path+file,'w')
    fs.writelines(res)
    fs.close()
    print('Successfully saved %s'%file)
    

################
    
#default_dir = 'E:/CIL_messages/'
default_dir = '/media/ky/easystore/CIL_messages/'
#cil_reader_dir = 'E:/cil_reader_data/'
#cil_checker_dir = 'E:/cil_checker_data/'
cil_reader_dir = '/media/ky/cil_reader_data/'
cil_checker_dir = '/media/ky/cil_checker_data/'

# sorts messages containing features by source ip address
def tag_by_src_ip(jsons, ip):
    return [j for j in jsons if j['src_ip'] == ip]
    
#sort by ip, and to subcateogires of each payloads
def sort_by_srcip_by_categories(json, ip):
    k=tag_by_src_ip(json,ip)
    tdic={'hello':[],'location':[],'detailed_performance':[],
                  'spectrum_usage':[],'incumbent':[],'cnt':0}
    hello=[]
    location=[]
    detailed_performance=[]
    spectrum_usage=[]
    incumbent=[]
    rest=[]
    for j in k:
        temp=j['cil_message']
        if 'hello' in temp:
            hello.append(temp)
        elif 'location_update' in temp:
            location.append(temp)
        elif 'detailed_performance' in temp:
            detailed_performance.append(temp)
        elif 'spectrum_usage'  in temp:
            spectrum_usage.append(temp)
        elif 'incumbent_notify' in temp:
            incumbent.append(temp)
        else:
            rest.append(temp)
    tdic['hello'] = hello
    tdic['location'] = location
    tdic['detailed_performance'] = detailed_performance
    tdic['spectrum_usage'] = spectrum_usage
    tdic['incumbent'] = incumbent
    tdic['else'] = rest
    return tdic

def sort_by_team(file_names, reader_path=dir_path+'cil_reader_data/scrimmage2/', checker_path=dir_path+'cil_checker_data/scrimmage2_fixed/'):
    team_numbers=[]
    cil_messages=[]
    for f in file_names:
        checker_file = open(checker_path+f,'r',encoding='utf-8')
        ip = get_ip(checker_file)
        checker_file.close()
        team_number = ''
        if 'Team' in f:
            for i in range(len(f)-6):
                if f[i:i+4] == 'Team':
                    team_number = f[i+4:i+6]
        elif 'jammer' in f:
            team_number = 'jammer'
        else:
            team_number = 'passive'
        team_numbers.append(team_number)
        with open(reader_path+f,'r',encoding='utf-8') as reader_file:
            k = reader_file.split('\n\n')
            cil_messages.append(sort_by_srcip_by_categories([json.loads(i) for i in k if i != ''],ip))
            reader_file.close()
    return [(team_numbers[i],cil_messages[i]) for i in range(len(team_numbers))]

import random
cil_message_by_team = sort_by_team(valid_files[-4:])


def tag_by_team(cil_message_sorted_team):
    lst_teams=[]
    for i in cil_message_sorted_team:
        lst_teams.append(i['team'])
    lst_teams = list(set(lst_teams))
    res = {}
    for t in lst_teams:
        temp=[]
        for k in cil_message_sorted_team:
            if k['team'] is t:
                temp.append(k['cil_message'])
        res[t] = temp
    return res

import random

#cil_message_by_team = tag_by_team([sort_by_team(i) for i in random.sample(valid_files,10)])