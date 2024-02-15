#Torch 2.0 tips and improvements:
    
#Compile a model for it to run faster:
from torch import nn
model = nn.Sequential(.....)
torch.compile(model)

#Set default device globally:
device = 'cuda:0' if torch.cuda.is_available() else "cpu"
torch.set_default_device(device)
#for display purposes switch to CPU:
torch.set_default_device('cpu')
#...or locally:
with torch.device(device):
    ...
#Retrieve model weights and transforms from torchvision ready models:
import torchvision
model_weights = torchvision.models.ResNet50_Weights.IMAGENET1K_V2
transforms = model_weights.transforms()


