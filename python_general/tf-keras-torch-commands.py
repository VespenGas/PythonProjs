#Machine learning libs - GPU highly recommended
#Linux environment required


#%%
#Tensorflow
import tensorflow as tf

print(tf.__version__)
print(tf.sysconfig.get_build_info())
#tf.compat.v1.Session()
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))
print(sess)
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
    capabilityGPU = tf.config.experimental.get_device_details(GPUs[0]).get("compute_capability")
    capabilityGPU = float(str(capabilityGPU[0]) + '.' + str(capabilityGPU[1]))
    print(f'Compute capability: {capabilityGPU}')
    assert capabilityGPU>3.5, 'CUDA compute capabiility lower than 3.5'

#Clear GPU memory
from keras import backend as K
K.clear_session()

#%%
#Pytorch
import torch
print(torch.cuda.is_available())
if torch.cuda.is_available():
    total_free_mem, total_mem = torch.cuda.mem_get_info("cuda:0")
    print(f'Total free GPU memory is: {total_free_mem/1024**2} MB')
    print(f'Total GPU memory is: {total_mem/1024**2} MB')
else:
    print("GPU not available!")

#if CUDA out of memory, set:
#os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:<enter-size-here>"
