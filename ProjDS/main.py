#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#%%
import pandas as pd
import geopandas as gpd
import os
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import torch
import torch.nn.functional as F
import kmeans_pytorch
from importlib import reload


print(f'Cuda available: {torch.cuda.is_available()}')
torch.cuda.empty_cache()
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
print('GPU available' if device=='cuda:0' else 'CPU available')
dtype = torch.float32 if device == 'cuda:0' else torch.float64

#-----------------------------------------------------------------------------
def get_columns(raw_df, column_names:list[str]):
    return_df = pd.DataFrame()
    for column_name in column_names:
        head = '<' + column_name + '>'
        tail = '</' + column_name + '>'
        return_df[column_name] = raw_df.str.partition(head)[2].str.partition(tail)[0]
    return return_df

def parse_fs_php(content:str, columns:list[str]):
    '''\
    Column names can be: "pubDate", "title", "description", "link", "geo:lat", "geo:long"
    '''
    content = content.rpartition('</item>')[0].partition('<item>')[2].split('</item><item>')
    content = pd.DataFrame(content).iloc[:,0].str.strip('\n\t\t\t')
    content = get_columns(content, columns)
    return content
def kmeans_torch(X, k, max_iters=100, device='cuda:0'):
    X = X.to(device)
    centroids_idx = torch.randperm(X.size(0))[:k]
    centroids = X[centroids_idx]

    for _ in range(max_iters):
        distances = torch.cdist(X, centroids, p=2)
        labels = torch.argmin(distances, dim=1)
        for i in range(k):
            if torch.sum(labels == i) > 0:
                centroids[i] = torch.mean(X[labels == i], dim=0)
    return centroids, labels
#-----------------------------------------------------------------------------
assert os.path.isfile('countrywide.csv'), 'countrywide.csv file is missing from the current working directory'
assert os.path.isfile('stations-georss.php'), 'stations-georss.php file is missing from the current working directory'

print('Reading file contents...')
client_locs = pd.read_csv('countrywide.csv')
client_locs = client_locs[['LON', 'LAT', 'REGION']]
with open('stations-georss.php', 'r') as file:
    php_contents = file.read()

#Process column structure

use_nsw_only = True

fs_df = parse_fs_php(php_contents, ['title', 'geo:lat', 'geo:long'])
fs_df[['geo:lat', 'geo:long']] = fs_df[['geo:lat', 'geo:long']].astype(float)
client_locs[['LON', 'LAT']] = client_locs[['LON', 'LAT']].astype(float)
fs_df[['geo:lat', 'geo:long']].round(6)
fs_df['title'] = fs_df['title'].str.rstrip(' Fire Station')
client_locs.columns = [x.lower() for x in client_locs.columns]
fs_df.rename(columns={'geo:lat' : 'lat', 'geo:long' : 'lon'}, inplace=True)

fs_df = fs_df.dropna()
client_locs = client_locs.dropna()

if use_nsw_only==True:
    client_locs = client_locs[client_locs['region']=='NSW']
    

print('Dataframe example data:\n')
print('Clients:\n')
print(client_locs.head(10))
print(f'>There are {client_locs.shape[0]} clients in the area.\n')

print('\nServices:\n')
print(fs_df.head(10))
print(f'>There are {fs_df.shape[0]} services in the area.\n')

#%%
#Read GPD shapefile
print("\nExtracting shapefile (Australia)...\n")
assert os.path.isdir("AU_SPF"), 'No Australia shapefile found'

australia = gpd.read_file('AU_SPF/STE_2021_AUST_GDA2020.shp').set_index('STE_CODE21')
if use_nsw_only==True:
    print('Setting geoplot to NSW only')
    australia = australia[australia['STE_NAME21']=='New South Wales']
australia = australia['geometry']

#print(australia.crs)
#print(australia.columns)

#%%
#Print Australia image + fire stations
print('\nPlotting...')
scale=6
_size=0.5
if not os.path.isfile('NSW_FS_client_KDE.png'):
    _figsize = np.asarray(matplotlib.rcParams['figure.figsize'])
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=_figsize*scale)
    fs_plot = sns.scatterplot(ax = ax, data=fs_df, x='lon', y='lat', legend=False, zorder=3, s=scale**(1.5)*_size*10)
    
    australia.plot(ax = ax, color='lightgrey', edgecolor='grey', linewidth=scale/3, zorder=1)
    
    #sns.scatterplot(ax = ax, data=client_locs, x='lon', y='lat', zorder=2, s=scale**(1.5)*_size*2, color='red')
    sns.kdeplot(data=client_locs, x='lon', y='lat', fill=True,
                cmap='coolwarm',
                alpha=0.2,
                #linewidth=0,
                levels=30, thresh=0.01,
                ax=ax)
    fig.get_figure().savefig("NSW_FS_client_KDE.png")
else:
    print('Plot already exists')
#%%
#Apply k-means clustering with GridSearchCV

#Test mode (less compute time) - only 100000 addresses
test_mode = False
silhouette_multiplier = 0.1
use_abstract_clusters=False

if test_mode == True:
    client_locs_train = client_locs[['lon', 'lat']].sample(n=1000000).to_numpy()
else:
    client_locs_train = client_locs[['lon', 'lat']].to_numpy()

if use_abstract_clusters==True:
    _n_clusters_init = int((client_locs_train.shape[0]**(0.5)+1)/10)
    _n_clusters_list = list(range(_n_clusters_init, _n_clusters_init*10, 25))
else:
    _n_clusters_list = [fs_df.shape[0]]


result_df = pd.DataFrame(columns=['number_of_clients', 'number_of_clusters', 'silhouette_score', 'calinski_harabasz_score', 'davies_bouldin_score'])
print(f'N Clusters are {_n_clusters_list}')
#For Torch implementation
x = torch.from_numpy(client_locs_train)

for _n_clusters in _n_clusters_list:
    torch.cuda.empty_cache()
    reload(kmeans_pytorch)
    import kmeans_pytorch
    if test_mode==True and device != "cpu":
        #Torch implementation (custom)
        cluster_centers, cluster_inference = kmeans_torch(X=x, k=_n_clusters, device=device)
        cluster_centers = cluster_centers.cpu().numpy()
        cluster_inference = cluster_inference.cpu().numpy()
        
        print(f'\nNumber of clusters: {_n_clusters} for {client_locs_train.shape[0]} entries.')
        silhouette = silhouette_score(client_locs_train, cluster_inference, sample_size=int(client_locs_train.shape[0]*silhouette_multiplier))
        print(f'Silhouette score - Torch, custom - {silhouette} - Best is 1 - Worst is -1')
        calinski_harabasz = calinski_harabasz_score(client_locs_train, cluster_inference)
        print(f'Calinski Harabasz score - Torch, custom - {calinski_harabasz} - Higher is better')
        davies_bouldin = davies_bouldin_score(client_locs_train, cluster_inference)
        print(f'Davies Bouldin score - Torch, custom - {davies_bouldin} - Best is 0')
        
        #Torch implementation (lib)
        cluster_inference, cluster_centers = kmeans_pytorch.kmeans(
        X=x, num_clusters=_n_clusters, distance='euclidean', device=torch.device('cuda:0'), tol=1e-4)
        print(f'\nNumber of clusters: {_n_clusters} for {client_locs_train.shape[0]} entries.')
        silhouette = silhouette_score(client_locs_train, cluster_inference, sample_size=int(client_locs_train.shape[0]*silhouette_multiplier))
        print(f'Silhouette score - Torch, lib - {silhouette} - Best is 1 - Worst is -1')
        calinski_harabasz = calinski_harabasz_score(client_locs_train, cluster_inference)
        print(f'Calinski Harabasz score - Torch, lib - {calinski_harabasz} - Higher is better')
        davies_bouldin = davies_bouldin_score(client_locs_train, cluster_inference)
        print(f'Davies Bouldin score - Torch, lib - {davies_bouldin} - Best is 0')
        
        #SKLearn implementation (comparison)
        
    model = KMeans(n_clusters=_n_clusters, max_iter=500, n_init=10, tol=1e-4)
    cluster_inference_sk = model.fit_predict(client_locs_train)
    print(f'\nNumber of clusters (SKLearn): {_n_clusters}')
    silhouette = silhouette_score(client_locs_train, cluster_inference_sk, sample_size=int(client_locs_train.shape[0]*silhouette_multiplier))
    print(f'Silhouette score (SKLearn) - {silhouette} - Best is 1 - Worst is -1')
    calinski_harabasz = calinski_harabasz_score(client_locs_train, cluster_inference_sk)
    print(f'Calinski Harabasz score (SKLearn) - {calinski_harabasz} - Higher is better')
    davies_bouldin = davies_bouldin_score(client_locs_train, cluster_inference_sk)
    print(f'Davies Bouldin score (SKLearn) - {davies_bouldin} - Best is 0')
            
    #%%
    temp_dict = {'number_of_clients':client_locs_train.shape[0], 'number_of_clusters':_n_clusters,
                'silhouette_score':silhouette,
                'calinski_harabasz_score':calinski_harabasz,
                'davies_bouldin_score':davies_bouldin,
                #'cluster_center':cluster_centers,
                }
    
    result_df.loc[len(result_df)] = pd.Series({'number_of_clients':client_locs_train.shape[0],
                                               'number_of_clusters':_n_clusters,
                                               #'silhouette_score':silhouette, 
                                               'calinski_harabasz_score':calinski_harabasz,
                                               'davies_bouldin_score':davies_bouldin})
print('\nDF created:\n')
print(result_df.head(5))

#%%
result_df.to_csv('df_k_means_metrics.csv')




