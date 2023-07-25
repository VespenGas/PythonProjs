#This model is very inaccurate

import torch
import requests
from pathlib import Path, PosixPath
import zipfile
import os
from PIL import Image
from torch.utils.data import DataLoader
from torchvision import transforms, datasets
from torch import nn
from torchinfo import summary
#from helper_functions import accuracy_fn
from torchmetrics.classification import MulticlassAccuracy
from tqdm import tqdm
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:5128"

device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
RANDOM_SEED = 42
torch.manual_seed(RANDOM_SEED)
torch.cuda.manual_seed(RANDOM_SEED)
BATCH_SIZE = 32
NUM_EPOCHS = 5


#Download a custom dataset if it does not exist:
data_path = os.path.join(os.getcwd(), 'data')
image_path = os.path.join(data_path, 'pizza_steak_sushi')
if not os.path.isdir(image_path):
    os.makedirs(image_path)
    print('Directory missing, created, downloading required dataset...')
    load_file = os.path.join(data_path, 'pizza_steak_sushi.zip')
    with open(load_file, 'wb') as f:
        request = requests.get("https://github.com/mrdbourke/pytorch-deep-learning/raw/main/data/pizza_steak_sushi.zip")
        f.write(request.content)
    with zipfile.ZipFile(load_file) as file:
        file.extractall(image_path)
else:
    print('Directory exists')

#Setting test train directories
train_path = os.path.join(image_path, 'train')
test_path = os.path.join(image_path, 'test')

#Test attempt to acquire all files without Pathlib
'''
all_dirs = []
all_dirnames = []
all_files = []
all_required_filepaths = []
for dirpaths, dirnames, filenames in os.walk(image_path):
    all_dirs.extend(dirpaths.split('\n'))
    all_dirnames.extend(dirnames)
    all_files.extend(filenames)
for dirpath in all_dirs:
    for filename in all_files:
        if os.path.isfile(os.path.join(dirpath, filename)):
            current_file = os.path.join(dirpath, filename)
            all_required_filepaths.append(current_file)
print(all_required_filepaths)
'''
#Using Pathlib:

image_path = PosixPath(image_path)
images = list(image_path.glob('*/*/*.jpg'))

#Executing image lib -> dataset -> data loader

train_data_transform = transforms.Compose([
    transforms.Resize((64, 64)),
    #transforms.RandomHorizontalFlip(p=0.5),
    transforms.TrivialAugmentWide(num_magnitude_bins=11),
    transforms.ToTensor()
    ])
test_data_transform = transforms.Compose([
    transforms.Resize((64, 64)),
    #transforms.RandomHorizontalFlip(p=0.5),
    #transforms.TrivialAugmentWide(num_magnitude_bins=31),
    transforms.ToTensor()
    ])

train_set_aug = datasets.ImageFolder(root=train_path, transform=train_data_transform)
test_set = datasets.ImageFolder(root=test_path, transform=test_data_transform, target_transform=None)

class_names = train_set_aug.classes
class_dict = train_set_aug.class_to_idx

train_dataloader = DataLoader(dataset=train_set_aug, batch_size=BATCH_SIZE, shuffle=True, num_workers=os.cpu_count())
test_dataloader = DataLoader(dataset=test_set, batch_size=BATCH_SIZE, num_workers=os.cpu_count())
#print(next(iter(train_dataloader)))

class TinyVGG(nn.Module):
    def __init__(self, input_shape=3, hidden_layers=30, output_shape = 3):
        super().__init__()
        self.sequential_model = nn.Sequential(
            nn.Conv2d(input_shape, hidden_layers, kernel_size = 3, stride = 1, padding=1),
            nn.GELU(),
            nn.Conv2d(hidden_layers, hidden_layers, kernel_size = 3, stride = 1, padding=1),
            nn.GELU(),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False),
            nn.Conv2d(hidden_layers, hidden_layers, kernel_size = 3, stride = 1, padding=1),
            nn.GELU(),
            nn.Conv2d(hidden_layers, hidden_layers, kernel_size = 3, stride = 1, padding=1),
            nn.GELU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Flatten(),
            nn.Linear(in_features=hidden_layers*16*16, out_features=3)
            )
    def forward(self, x):
        return self.sequential_model(x)
model = TinyVGG(input_shape = 3, hidden_layers=10, output_shape=len(class_names)).to(device)
#print(summary(model, input_size = [1,3,64,64]))

accuracy_fn = MulticlassAccuracy(len(class_names)).to(device)


#define train and test functions
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
        train_acc += accuracy_fn(y_pred.argmax(dim=1), y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    train_loss /= len(data_loader)
    train_acc /= len(data_loader)    
    print(f"Train loss: {train_loss:.5f} | Train accuracy: {train_acc*100:.2f}%")
def test_step(data_loader: torch.utils.data.DataLoader,
              model: torch.nn.Module, loss_fn: torch.nn.Module,
              accuracy_fn, device: torch.device = device):
    test_loss, test_acc = 0, 0    
    model.to(device)
    model.eval()
    with torch.inference_mode():         
        for X, y in data_loader:
            X, y = X.to(device), y.to(device)
            test_pred = model(X)     
            test_loss += loss_fn(test_pred, y)
            test_acc += accuracy_fn(test_pred.argmax(dim=1), y)
        test_loss /= len(data_loader)
        test_acc /= len(data_loader)        
        print(f"Test loss: {test_loss:.5f} | Test accuracy: {test_acc*100:.2f}%\n")
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(params=model.parameters(), lr=0.01)

for epoch in tqdm(range(NUM_EPOCHS)):
    train_step(
        model=model,
        data_loader=train_dataloader,
        loss_fn=loss_fn,
        optimizer=optimizer,
        accuracy_fn=accuracy_fn
        )
    test_step(
        model=model,
        data_loader=train_dataloader,
        loss_fn=loss_fn,
        accuracy_fn=accuracy_fn
        )



