#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 14:57:34 2024

@author: eugen
"""

import pandas as pd
import numpy as np
import warnings
import tensorflow as tf
from tensorflow import keras
pd.set_option('display.max_columns', 120)
warnings.filterwarnings('ignore')

from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Normalization, Dropout

def percent_of_nan_rows(dataset:pd.DataFrame, column:str) -> float:
    return len(X[X[column].isna()]) / len(X) * 100

GPUs = tf.config.list_physical_devices('GPU')
if GPUs:
    print(f'GPU data: {tf.config.experimental.get_device_details(GPUs[0])}')
    for GPU in GPUs:
        tf.config.experimental.set_memory_growth(GPU, True)
else:
    print('No GPUs detected!')
CPUs = tf.config.list_physical_devices('CPU')
print(f'CPU is: {tf.config.experimental.get_device_details(CPUs[0])}')

myocardial_infarction_complications = fetch_ucirepo(id=579)
X = myocardial_infarction_complications.data.features
y = myocardial_infarction_complications.data.targets

X = X.fillna(np.nan)
vars_ = pd.DataFrame(myocardial_infarction_complications.variables)
cat_cols = vars_[(vars_['role'] == 'Feature') & (vars_['type'] == 'Categorical')]['name'].tolist()
bin_cols = vars_[(vars_['role'] == 'Feature') & (vars_['type'] == 'Binary')]['name'].tolist()
int_cols = vars_[(vars_['role'] == 'Feature') & (vars_['type'] == 'Integer')]['name'].tolist()
float_cols = vars_[(vars_['role'] == 'Feature') & (vars_['type'] == 'Continuous')]['name'].tolist()
X.drop(index = X[X.count(axis=1)<len(X.columns)*0.7].index, inplace=True)
for column in X.columns:
    if percent_of_nan_rows(X, column) > 75:
        X.drop(columns = [column], inplace=True)
        try:
            bin_cols.remove(column)
        except:
            pass
        try:
            cat_cols.remove(column)
        except:
            pass
        try:
            int_cols.remove(column)
        except:
            pass
        try:
            float_cols.remove(column)
        except:
            pass
    else:
        if column in cat_cols or column in bin_cols:
            names = X[column].value_counts().index.tolist()
            weights = X[column].value_counts().tolist()/X[column].count()
            X[column] = X[column].apply(lambda l: l if not np.isnan(l) else np.random.choice(names, p=weights))
            pass
        else:
            X[column] = X[column].apply(lambda l: l if not np.isnan(l) else X[column].mean() + np.random.random()*2*X[column].std())
            X[column] = X[column].apply(lambda l: (l-X[column].mean())/X[column].std())
            pass
X[bin_cols] = X[bin_cols].applymap(lambda x: bool(x))
X = pd.get_dummies(data = X, columns = cat_cols)
bin_cols_preds = vars_[(vars_['role'] == 'Target') & (vars_['type'] == 'Binary')]['name'].tolist()
cat_cols_preds = vars_[(vars_['role'] == 'Target') & (vars_['type'] == 'Categorical')]['name'].tolist()
y[bin_cols_preds] = y[bin_cols_preds].applymap(lambda x: bool(x))
y = pd.get_dummies(data = y, columns = cat_cols_preds)
data = X.merge(y, left_index=True, right_index=True)

data = pd.concat([data[data['LET_IS_0'] == False], data[data['LET_IS_0'] != False].sample(int(len(data[data['LET_IS_0'] == False])))])
#data = data[data['LET_IS'] != 0]
X = data[X.columns]
y = data[y.columns]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=True
    )

X_train = np.asarray(X_train).astype(float)
y_train = np.asarray(y_train).astype(float)
X_test = np.asarray(X_test).astype(float)
y_test = np.asarray(y_test).astype(float)

normalizer = Normalization(axis=-1)
normalizer.adapt(X_train)

model = Sequential([
    normalizer,
    Dense(200),
    Activation('gelu'),
    Dropout(0.1),
    Dense(500),
    Activation('gelu'),
    Dropout(0.1),
    Dense(19),
    #Dense(12),
    Activation('softmax'),
    ])
model.compile(optimizer=keras.optimizers.legacy.RMSprop(learning_rate=1e-5), loss=keras.losses.CategoricalCrossentropy(), metrics=['categorical_accuracy'])
model.fit(X_train, y_train, epochs=20, batch_size=32)

metrics = model.evaluate(X_test, y_test, batch_size=32)
y_pred = model.predict(X_test)


