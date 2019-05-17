# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 12:22:46 2019

@author: KY-Coffee
"""

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def plot_KMeans(k_data,n=14, title="", margins=True):
    model = KMeans(n)
    model.fit(k_data[0])
    
    y_kmeans = model.predict(k_data[0])
    plt.figure(figsize=(10,5))
    plt.title("KMeans clustering result for n = "+str(n)+ " "+title)
    #plt.xlabel("Predicted")
    #plt.ylabel("Actual")
    if margins:
        plt.axis([0,10,0,20])
    plt.scatter(k_data[0][:, 0], k_data[0][:, 1], c=y_kmeans, s=50, cmap='viridis')
    plt.legend(y_kmeans)
    #plt.scatter(all_prediction,range(1,len(all_prediction)+1))