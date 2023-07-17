#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import torch
from torch import nn
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
#Generate arbitrary linear data
weight = 0.7
bias = 0.3
X = torch.arange(0, 1, 0.02).unsqueeze(dim=1)
y = weight * X + bias
#Train-test split
split_percent = 0.8
split_point = int(len(y) * split_percent)
X_train, y_train, X_test, y_test = X[:split_point], y[:split_point], X[split_point:], y[split_point:]
print(X_train, y_train, X_test, y_test)


class LinearModelV2(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_layer = nn.Linear(in_features=1, out_features=1)
    def forward(self, x):
        return self.linear_layer(x)
#Equivalent class is:
'''
class LinearModelV2(nn.Module):
    def __init__(self):
        super().__init__()
        self.weights = nn.Parameter(torch.randn(1, dtype=torch.float64), requires_grad=True)
        self.bias = nn.Parameter(torch.randn(1, dtype=torch.float64), requires_grad=True)
    def forward(self, x):
        return self.weights * x + self.bias
'''

torch.manual_seed(42)
model = LinearModelV2()
model.to(device)
X_test.to(device)
X_train.to(device)
y_test.to(device)
y_train.to(device)
loss = nn.L1Loss()
optimizer = torch.optim.SGD(params = model.parameters(), lr=0.01)
epochs = 100
for epoch in range(epochs):
    model.train()
    y_pred = model(X_train)
    loss_val = loss(y_pred, y_train)
    optimizer.zero_grad()
    loss_val.backward()
    optimizer.step()
    model.eval()
    with torch.inference_mode():
        test_pred = model(X_test)
        test_loss = loss(test_pred, y_test)
        print(f'Test loss at {epoch} is {test_loss} and test prediction is {test_pred}.')
        
model.eval()
with torch.inference_mode():
    y_pred = model(X_test)
print('=' * 80)
print(y_pred)



