# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 12:59:47 2019

@author: ky
"""

import numpy as np
from sklearn.cluster import KMeans

Kmean = KMeans(n_clusters=18)
Kmean.fit(X)