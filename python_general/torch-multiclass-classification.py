import torch
from torch import nn
import pandas
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
import torchmetrics

import requests 
from pathlib import Path  
 
# Download helper functions from Learn PyTorch repo (if not already downloaded) 
if Path("helper_functions.py").is_file(): 
  print("helper_functions.py already exists, skipping download") 
else: 
  print("Downloading helper_functions.py") 
  request = requests.get("https://raw.githubusercontent.com/mrdbourke/pytorch-deep-learning/main/helper_functions.py") 
  with open("helper_functions.py", "wb") as f: 
    f.write(request.content) 

from helper_functions import plot_decision_boundary

device = 'cuda' if torch.cuda.is_available() else 'cpu'

NUM_CLASSES = 4
NUM_FEATURES = 2
RANDOM_SEED = 42
X_blob, y_blob = make_blobs(n_samples=1000, n_features=NUM_FEATURES, centers=NUM_CLASSES, 
                            cluster_std=1.5, random_state=RANDOM_SEED)
X_blob = torch.tensor(X_blob).type(torch.float32)
y_blob = torch.tensor(y_blob).type(torch.LongTensor)

X_blob_train, X_blob_test, y_blob_train, y_blob_test = train_test_split(
    X_blob, y_blob, test_size=0.2, random_state=RANDOM_SEED
    )
plt.scatter(X_blob[:,0], X_blob[:, 1], c=y_blob, cmap=plt.cm.RdYlBu)
plt.show()

class BlobModel(nn.Module):
    def __init__(self, input_features, output_features, hidden_units=10):
        super().__init__()
        self.input_features = input_features
        self.output_features = output_features 
        self.hidden_units = hidden_units
        self.linear_layer_stack = nn.Sequential(
            nn.Linear(in_features=self.input_features, out_features=self.hidden_units),
            nn.GELU(),
            nn.Linear(in_features=self.hidden_units, out_features=self.hidden_units),
            nn.GELU(),
            nn.Linear(in_features=self.hidden_units, out_features=self.output_features)
            )
    def forward(self, x):
        return self.linear_layer_stack(x)
    
model = BlobModel(NUM_FEATURES, NUM_CLASSES, hidden_units=30).to(device)
X_blob_train = X_blob_train.to(device)
X_blob_test = X_blob_test.to(device)
y_blob_train = y_blob_train.to(device)
y_blob_test = y_blob_test.to(device)
print(X_blob_train.shape, X_blob_test.shape, y_blob_train.shape, y_blob_test.shape)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
metric = torchmetrics.classification.MulticlassAccuracy(NUM_CLASSES).to(device)
epochs = 10
for epoch in range(epochs+1):
    y_logits = model(X_blob_train).squeeze()
    y_pred = torch.softmax(y_logits, dim=1).argmax(dim=1)
    loss = loss_fn(y_logits, y_blob_train)
    acc = metric(y_pred, y_blob_train)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    model.eval()
    with torch.inference_mode():
        test_logits = model(X_blob_test)
        test_pred = torch.softmax(test_logits, dim=1).argmax(dim=1)
        test_loss = loss_fn(test_logits, y_blob_test)
        test_acc = metric(test_pred, y_blob_test)
        if epoch%10 == 0:
            print(f'Epoch: {epoch}, Loss: {loss}, Accuracy: {acc}, Test loss: {test_loss}')
    

plot_decision_boundary(model, X_blob_test, y_blob_test)

