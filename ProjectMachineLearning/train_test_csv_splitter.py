#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 16:01:33 2023

@author: eugen

This script create emulation train.csv and test.csv files from train_emotion.csv. 
Run it or add files manually to the directory of main_script.py.
"""

import os
import pandas as pd
assert os.path.isfile('train_emotion.csv'), 'No initial .csv file found. Please place the file in the directory with the script.'

train_fraction = 0.7

file = pd.read_csv('train_emotion.csv')
file = file.sample(frac=1)
train = file.iloc[0:int(len(file)*train_fraction)]
test = file.iloc[int(len(file)*train_fraction):]['text']
train.to_csv('train.csv', index=False)
test.to_csv('test.csv', index=False)
