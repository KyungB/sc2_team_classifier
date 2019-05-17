# -*- coding: utf-8 -*-
"""
Created on Mon May 13 01:34:20 2019

@author: KY-Coffee
"""

import json
import numpy as np
import feature_convert as fc
from os import listdir
from os.path import isfile, join

dir_path = '/media/ky/easystore/'
#dir_path = 'E:/'

# Recieves opened file as input
def get_ip(checker_file, path=dir_path+'/cil_checker_data/scrimmage2_fixed/'):
    return str(json.load(checker_file)[0]['sender_ip_address'])

### get rid of unnecessary portion from cil_checker --auto data
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
    
#default_dir = 'E:/CIL_messages/'
default_dir = '/media/ky/easystore/CIL_messages/'
#cil_reader_dir = 'E:/cil_reader_data/'
#cil_checker_dir = 'E:/cil_checker_data/'
cil_reader_dir = '/media/ky/cil_reader_data/'
cil_checker_dir = '/media/ky/cil_checker_data/'

onlyfiles_scrimmage2 = [f for f in listdir(dir_path+'/cil_reader_data/scrimmage2/') 
                if isfile(join(dir_path+'/cil_reader_data/scrimmage2/', f))]
checker_scrimmage2 = [f for f in listdir(dir_path+'/cil_checker_data/scrimmage2/') 
                if isfile(join(dir_path+'/cil_checker_data/scrimmage2/', f))]

valid_files = [i for i in onlyfiles_scrimmage2 if i in checker_scrimmage2]

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


def tag_by_team(file_name, reader_path=dir_path+'cil_reader_data/scrimmage2/', checker_path=dir_path+'cil_checker_data/scrimmage2_fixed/'):
    checker_file = open(checker_path+file_name,'r',encoding='utf-8')
    ip = get_ip(checker_file)
    checker_file.close()
    team_number = ''
    if 'Team' in file_name:
        for i in range(len(file_name)-6):
            if file_name[i:i+4] == 'Team':
                team_number = file_name[i+4:i+6]
    elif 'jammer' in file_name:
        team_number = 'jammer'
    else:
        team_number = 'passive'
    
    reader_file = open(reader_path+file_name,'r')
    k = reader_file.read().split('\n\n')
    cil_messages = sort_by_srcip_by_categories([json.loads(i) for i in k if i != ''],ip)
    reader_file.close()
    features={'team':team_number}
    features['IA_gps'] = fc.interarrival_time_gps(cil_messages)
    features['IA_dp'] = fc.interarrival_time_detailed_performance(cil_messages)
    features['IA_voxel'] = fc.interarrival_time_voxel_forecast(cil_messages)
    return features


def sort_by_team(cil_message_tagged_team):
    lst_teams=[]
    for i in cil_message_tagged_team:
        lst_teams.append(i['team'])
    lst_teams = list(set(lst_teams))
    sorted_dic={}
    for t in lst_teams:
        messages = [i for i in cil_message_tagged_team if i['team'] == t]
        sorted_dic[t] = messages
    return sorted_dic

#import time
#st = time.time()
#tagged_team=[]
#for tt in valid_files:
#    tagged_team.append(tag_by_team(tt))
#tagged_team = sort_by_team(tagged_team)
#print("Time taken: %f"%(time.time()-st))

def make_data(teams):
    x=[]
    y=[]
    for team in teams.keys():
        if team not in ['passive','jammer']:
            team_num = int(team)
        else:
            team_num = 14
        for i in teams[team]:
            temp_x = [np.mean(i['IA_gps']), np.std(i['IA_gps']), np.mean(i['IA_dp']), np.std(i['IA_dp']), np.mean(i['IA_voxel']), np.std(i['IA_voxel'])]
            x.append(temp_x)
            y.append(team_num)

    return np.array(np.nan_to_num(x),dtype=np.float32), np.array(y,dtype=np.float32)

def train_and_visualize(x,y):
    from sklearn.model_selection import train_test_split
    
    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=1)
    
    from sklearn import tree
    model = tree.DecisionTreeClassifier()
    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)
    
    from sklearn.metrics import accuracy_score, f1_score
    
    print("Accuracy: ", accuracy_score(y_test, y_predict))
    print("F1 score: ",f1_score(y_test,y_predict,average='macro'))
    #roc_curve(y_test,y_predict)
    
    
    from sklearn import tree
    from IPython.display import SVG
    from graphviz import Source
    from IPython.display import display
    
    # Create DOT data
    graph = Source(tree.export_graphviz(model, out_file=None, 
                                        feature_names=['mean_gps','stdv_gps',
                                                       'mean_dp','stdv_dp','mean_voxel','stdv_voxel'],
                                            class_names=[str(c) for c in range(1,15)], 
                                            filled=True, special_characters=True))
    display(SVG(graph.pipe(format='svg')))
    
import pickle
tagged_team = pickle.load(open('tagged_team.p','rb'))
x,y = make_data(tagged_team)
