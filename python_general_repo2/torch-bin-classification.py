import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split
import torch
from torch import nn
from torcheval.metrics import BinaryAccuracy
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
 
from helper_functions import plot_predictions, plot_decision_boundary

device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.manual_seed(42)

X,y = make_circles(1000, noise=0.03, random_state=42)
circles = pd.DataFrame({
    'X1':X[:,0],
    'X2':X[:,1],
    'label':y
    })
plt.scatter(circles.X1, circles.X2, c=circles.label)
plt.show()
#Input and output shapes
print(X.shape, y.shape)
X = torch.from_numpy(X).type(torch.float32).to(device)
y = torch.from_numpy(y).type(torch.float32).to(device)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_test, y_train, y_test = (X_train.type(torch.float32).to(device), X_test.type(torch.float32).to(device), 
                                    y_train.type(torch.float32).to(device), y_test.type(torch.float32).to(device))

class ClassificationModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer_1 = nn.Linear(in_features=2, out_features=30)
        self.layer_2 = nn.Linear(in_features=30, out_features=30)
        self.layer_3 = nn.Linear(in_features=30, out_features=1)
        self.relu = nn.ReLU()
        self.sigm = nn.Sigmoid()
    def forward(self, x):
        return self.layer_3(self.relu(self.layer_2(self.relu(self.layer_1(x)))))
model = ClassificationModel().to(device)
#OR
model_0 = nn.Sequential(
    nn.Linear(in_features=2, out_features=10),
    nn.ReLU(),
    nn.Linear(in_features=10, out_features=10),
    nn.ReLU(),
    nn.Linear(in_features=10, out_features=1),
    nn.Sigmoid()
    ).to(device)
#print(model.state_dict())
#model and model_0 are equivalent

#Setup optimizer and loss
optimiser = torch.optim.SGD(params=model.parameters(), lr=0.1)
loss_fn = nn.BCEWithLogitsLoss()
#Create evaluation metric
metric = BinaryAccuracy().to(device)
epochs = 3000
for epoch in range(epochs+1):
    y_logits = model(X_train).squeeze()
    y_pred = torch.round(torch.sigmoid(y_logits))
    loss = loss_fn(y_logits, y_train)
    acc = metric.update(y_pred, y_train).compute()
    
    optimiser.zero_grad()
    loss.backward()
    optimiser.step()
    model.eval()
    with torch.inference_mode():
        test_logits = model(X_test).squeeze().to(device)
        test_pred = torch.round(torch.sigmoid(test_logits))
        test_loss = loss_fn(test_logits, y_test)
        test_metric = metric.update(test_pred, y_test).compute()
    if epoch%100==0:
        print(f'Epoch: {epoch}, Loss: {loss}, Accuracy: {acc}, Test Loss: {test_loss}')

#Plot
plot_decision_boundary(model, X_test, y_test)






