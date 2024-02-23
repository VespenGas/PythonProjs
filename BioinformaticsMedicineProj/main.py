#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 19:30:09 2024

@author: eugen
"""
import torch
import pandas as pd

from ucimlrepo import fetch_ucirepo
from torch import nn
from sklearn.model_selection import train_test_split

myocardial_infarction_complications = fetch_ucirepo(id=579)
X = myocardial_infarction_complications.data.features
y = myocardial_infarction_complications.data.targets

# metadata 
#print(myocardial_infarction_complications.metadata)
  
# variable information 
#print(myocardial_infarction_complications.variables)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.set_default_device(device)
print(f'The device is: {device}')


#torch.compile(model)
