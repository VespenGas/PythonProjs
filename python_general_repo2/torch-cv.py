from tqdm import tqdm
import torch
from torch import nn
import numpy as np
import matplotlib.pyplot as plt

from torchvision import datasets
from torchvision import transforms
import torchmetrics

device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
from helper_functions import accuracy_fn

def train_step(model: torch.nn.Module, data_loader: torch.utils.data.DataLoader,
               loss_fn: torch.nn.Module, optimizer: torch.optim.Optimizer,
               accuracy_fn, device: torch.device = device):
    train_loss, train_acc = 0, 0    
    model.to(device)
    for batch, (X, y) in enumerate(data_loader):
        X, y = X.to(device), y.to(device)
        y_pred = model(X)
        loss = loss_fn(y_pred, y)        
        train_loss += loss
        train_acc += accuracy_fn(y_true=y,                                 
                                 y_pred=y_pred.argmax(dim=1))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    train_loss /= len(data_loader)
    train_acc /= len(data_loader)    
    print(f"Train loss: {train_loss:.5f} | Train accuracy: {train_acc:.2f}%")
def test_step(data_loader: torch.utils.data.DataLoader,
              model: torch.nn.Module, loss_fn: torch.nn.Module,
              accuracy_fn, evice: torch.device = device):
    test_loss, test_acc = 0, 0    
    model.to(device)
    model.eval()
    with torch.inference_mode():         
        for X, y in data_loader:
            X, y = X.to(device), y.to(device)
            test_pred = model(X)     
            test_loss += loss_fn(test_pred, y)
            test_acc += accuracy_fn(y_true=y,                
                                    y_pred=test_pred.argmax(dim=1))
        test_loss /= len(data_loader)
        test_acc /= len(data_loader)        
        print(f"Test loss: {test_loss:.5f} | Test accuracy: {test_acc:.2f}%\n")


train_data = datasets.FashionMNIST(root = 'data', train=True,
                                   download=True, transform=transforms.ToTensor(), target_transform = None)

test_data = datasets.FashionMNIST(root='data', train=False,
                                  download=True, transform=transforms.ToTensor())

print(train_data[0][0].shape)
class_names = train_data.classes
print(class_names)
class CVModel(nn.Module):
    def __init__(self, in_shape: int, out_shape: int, hidden_layers: int):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Conv2d(in_channels = in_shape, out_channels = hidden_layers, kernel_size = 3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels = hidden_layers, out_channels = hidden_layers, kernel_size = 3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Conv2d(in_channels = hidden_layers, out_channels = hidden_layers, kernel_size = 3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels = hidden_layers, out_channels = hidden_layers, kernel_size = 3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Flatten(),
            nn.Linear(in_features = hidden_layers*49, out_features = out_shape)
            )
    def forward(self, x: torch.Tensor):
        return self.layers(x)
model = CVModel(in_shape=1, out_shape = len(class_names), hidden_layers=10)
model.state_dict()
train_dataset = torch.utils.data.DataLoader(train_data, batch_size = 32, shuffle=True)
test_dataset = torch.utils.data.DataLoader(test_data, batch_size = 32, shuffle=True)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(params=model.parameters(), lr=0.1)
#accuracy_fn = torchmetrics.Accuracy(task='multiclass', num_classes=10)
epochs = 3
for epoch in tqdm(range(epochs)):
    train_step(
        model=model,
        data_loader=train_dataset,
        loss_fn=loss_fn,
        optimizer=optimizer,
        accuracy_fn=accuracy_fn
        )
    test_step(
        model=model,
        data_loader=train_dataset,
        loss_fn=loss_fn,
        accuracy_fn=accuracy_fn
        )


