# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 00:02:39 2019

@author: KY-Coffee
"""

import numpy as np

import scipy.interpolate as ip

from scipy.interpolate import splrep, spleval, splev

import matplotlib.pyplot as plt



x0 = np.linspace(0, 10, 15)

y0 = np.cos(x0)



spl = splrep(x0, y0)

x1 = np.linspace(0, 10, 50)

y1 = splev(x1, spl)



plt.figure(figsize=(20, 5))



plt.subplot(121)

plt.plot(x0, y0, 'o')



plt.plot(x1, y1, 'r')

plt.grid()



plt.subplot(122)

y2=np.sin(x0)

spl2=splrep(x0, y2)

y3=splev(x1, spl2)

plt.plot(x0, y2, 'o')

plt.plot(x1, y3, 'b')

plt.grid()

plt.show()
