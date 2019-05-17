# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 14:24:09 2019

@author: ky
"""

import feature_convert as fc
import numpy as np
import process as pc

def cvt_ms(timestamp):
    return round(fc.ps_to_s(timestamp),1e-3)
    