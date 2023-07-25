#Machine learning libs - GPU highly recommended
#Linux environment required
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
import seaborn as sns
import matplotlib.pyplot as plt


#%%
#Tensorflow
print(tf.__version__)
print(tf.sysconfig.get_build_info())
tf.compat.v1.Session()

GPUs = tf.config.list_physical_devices('GPU')
if GPUs:
    print(f'GPU data: {tf.config.experimental.get_device_details(GPUs[0])}')
    for GPU in GPUs:
        tf.config.experimental.set_memory_growth(GPU, True)
else:
    print('No GPUs detected!')
CPUs = tf.config.list_physical_devices('CPU')
print(f'CPU is: {tf.config.experimental.get_device_details(CPUs[0])}')

#Check compute capability
if GPUs:
    print(torch.cuda.mem_get_info("cuda:0"))
    capabilityGPU = tf.config.experimental.get_device_details(GPUs[0]).get("compute_capability")
    capabilityGPU = float(str(capabilityGPU[0]) + '.' + str(capabilityGPU[1]))
    print(f'Compute capability: {capabilityGPU}')
    assert capabilityGPU>3.5, 'CUDA compute capabiility lower than 3.5'
var = tf.Variable(0, dtype=tf.int64)
matrix = tf.Variable([1,2,3], dtype=tf.int64)
const = tf.constant('value', dtype=tf.string)
tf.rank(matrix)
matrix.shape


#%%
#Pytorch
print(torch.cuda.is_available())
print(torch.zeros(1).cuda())

#if CUDA out of memory, set:
#os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:<enter-size-here>"

