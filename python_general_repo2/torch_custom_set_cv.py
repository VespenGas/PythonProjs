import torch
import requests
import torchvision
from pathlib import Path
import zipfile
import os
from PIL import Image

device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
RANDOM_SEED = 42

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






