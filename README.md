# sc2_team_classifier
Created by Kyunglok Baik

*Training data (for tag_ip.py) : tagged_team.p.zip -> must be unzipped to tagged_team.p before running.
-------------------------------------------------------------------
!! important : Please change directory path before running the files.

1. feature_convert.py : consists of functions that generate features
feature_convert2.py: extension of feature_convert.py

2. kmean.py : function that creates K-nearest-neighbor clustering plot
tsne_cluster.py : function that creates t-Distributed Stochastic Neighbor Embedding clustering plot

3. plot_graphs : creates feature plots

4. process.py : process raw output (.json) format from cil_tool

5. seq_lstm.py : create lstm sequence model

6. tag_ip.py : create a supervised Decision Tree classifier & training sets based on scrimmage 2 data

---------------------------------------------------------------------

Bash scripts to download .pcap files & operate cil tool 

(must activate cil_tool beforehand)-----------------------------------

1. download_freeplay.sh : download freeplay from church server using rsync (must change the user name beforehand)

(must be placed in scrimmage 2 data folder & requires cil_tool activation beforehand)-----------------

2. tag_scrimmage2.sh :  generates tagged cil_chekcer data to that will later be used to extract team IP address for training/testing set generation purposes

3. cvt_cil_message.sh : generates cil messages data and saves to .json format by going through each folders
