#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 19:30:09 2024

@author: eugen
"""

import torch
import torchmetrics
import pandas as pd
import numpy as np
import warnings
pd.set_option('display.max_columns', 120)
warnings.filterwarnings('ignore')

from ucimlrepo import fetch_ucirepo
from torch import nn
from sklearn.model_selection import train_test_split

def percent_of_nan_rows(dataset:pd.DataFrame, column:str) -> float:
    return len(X[X[column].isna()]) / len(X) * 100

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
            pass
X[bin_cols] = X[bin_cols].applymap(lambda x: bool(x))
X = pd.get_dummies(data = X, columns = cat_cols)
bin_cols_preds = vars_[(vars_['role'] == 'Target') & (vars_['type'] == 'Binary')]['name'].tolist()
cat_cols_preds = vars_[(vars_['role'] == 'Target') & (vars_['type'] == 'Categorical')]['name'].tolist()
y[bin_cols_preds] = y[bin_cols_preds].applymap(lambda x: bool(x))
y = pd.get_dummies(data = y, columns = cat_cols_preds)
data = X.merge(y, left_index=True, right_index=True)
X = data[X.columns]
y = data[y.columns]

device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.set_default_device(device)
print(f'The device is: {device}')

class BioModel(nn.Module):
    def __init__(self, input_features, output_features, hidden_units=500):
        super().__init__()
        self.input_features = input_features
        self.output_features = output_features 
        self.hidden_units = hidden_units
        self.linear_layer_stack = nn.Sequential(
            nn.Linear(in_features=self.input_features, out_features=self.hidden_units*2),
            nn.GELU(),
            nn.Linear(in_features=self.hidden_units*2, out_features=self.hidden_units*2),
            nn.GELU(),
            nn.Linear(in_features=self.hidden_units*2, out_features=self.hidden_units),
            nn.GELU(),
            nn.Linear(in_features=self.hidden_units, out_features=self.hidden_units),
            nn.ReLU(),
            nn.Linear(in_features=self.hidden_units, out_features=self.output_features),
            nn.Softmax(),
            )
    def forward(self, x):
        return self.linear_layer_stack(x)

NUM_FEATURES = X.shape[1]
NUM_CLASSES = y.shape[1]

model = BioModel(NUM_FEATURES, NUM_CLASSES)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=True
    )
X_train = torch.tensor(X_train.values.astype(float)).type(torch.float32)
y_train = torch.tensor(y_train.values.astype(float)).type(torch.float32)
X_test = torch.tensor(X_test.values.astype(float)).type(torch.float32)
y_test = torch.tensor(y_test.values.astype(float)).type(torch.float32)
loss_fn = nn.CrossEntropyLoss()
#loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, weight_decay=0.005)
#metric = torchmetrics.classification.MulticlassAccuracy(NUM_CLASSES)
torch.compile(model)
epochs = 30
for epoch in range(epochs+1):
    y_pred = model(X_train)
    loss = loss_fn(y_pred, y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    model.eval()
    with torch.inference_mode():
        test_pred = model(X_test)
        test_loss = loss_fn(test_pred, y_test)
        #test_acc = metric(test_pred, y_test)
        if epoch%10 == 0:
            print(f'Epoch: {epoch}, Loss: {loss}, Test loss: {test_loss}')



