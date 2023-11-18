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
import kmeans_pytorch
from importlib import reload
import multiprocessing
import itertools
import platform
import subprocess
import re
from scipy.spatial import Voronoi, voronoi_plot_2d
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset


print(f'Cuda available: {torch.cuda.is_available()}')
torch.cuda.empty_cache()
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
print('GPU available' if device=='cuda:0' else 'CPU available')
dtype = torch.float32 if device == 'cuda:0' else torch.float64

#-----------------------------------------------------------------------------
def get_processor_name():
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command ="sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(command).strip()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).decode().strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub( ".*model name.*:", "", line,1)
    return ""
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
def get_data_fraction(data, *, cv, fraction_id):
    assert fraction_id<=cv, "Requested fraction ID higher than fractions amount"
    len_of_fraction = int(data.shape[0]/cv)
    return data[len_of_fraction*fraction_id:len_of_fraction*(fraction_id+1), 0:]
def perform_k_means(client_locs_train, cv, fraction_id, _n_clusters):
    data = get_data_fraction(client_locs_train, cv=cv, fraction_id=fraction_id)
    print(f'FractionID is: {fraction_id} with {data.shape[0]} entries.')
    model = KMeans(n_clusters=_n_clusters, max_iter=500, n_init=10, tol=1e-4)
    model.fit_predict(data)
    labels = model.labels_
    centroids = model.cluster_centers_
    
    print(f'\nNumber of clusters (SKLearn): {_n_clusters}')
    silhouette = silhouette_score(data, labels)
    print(f'Silhouette score (SKLearn) - {silhouette} - Best is 1 - Worst is -1')
    calinski_harabasz = calinski_harabasz_score(data, labels)
    print(f'Calinski Harabasz score (SKLearn) - {calinski_harabasz} - Higher is better')
    davies_bouldin = davies_bouldin_score(data, labels)
    print(f'Davies Bouldin score (SKLearn) - {davies_bouldin} - Best is 0')
    
    out = pd.Series({
        'data_fraction_ID':fraction_id,
        'number_of_clients_fractured':data.shape[0], 
        'number_of_clusters':_n_clusters,
        'silhouette_score':silhouette,
        'calinski_harabasz_score':calinski_harabasz,
        'davies_bouldin_score':davies_bouldin,
        'cluster_center':centroids
        })
    return out
#-----------------------------------------------------------------------------
if "Intel" in get_processor_name():
    from sklearnex import patch_sklearn
    patch_sklearn()

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

if use_nsw_only:
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
x1, x2, y1, y2 = 150, 152, -35, -32.5
_figsize = np.asarray(matplotlib.rcParams['figure.figsize'])
if not os.path.isfile('NSW_FS_client_KDE.png'):
    print('Creating KDE plot - this may take time (up to 1 hour)')
    sns.set_style("whitegrid")
    fig, (ax, ax0) = plt.subplots(ncols = 2, figsize=_figsize*scale)
    fs_plot = sns.scatterplot(ax = ax, data=fs_df, x='lon', y='lat', legend=False, zorder=3, s=scale**(1.5)*_size*5)
    australia.plot(ax = ax, color='lightgrey', edgecolor='grey', linewidth=scale/3, zorder=1)
    
    #sns.scatterplot(ax = ax, data=client_locs, x='lon', y='lat', zorder=2, s=scale**(1.5)*_size*2, color='red')
    sns.kdeplot(data=client_locs, x='lon', y='lat', fill=True,
                cmap='coolwarm',
                alpha=0.2,
                #linewidth=0,
                levels=30, thresh=0.01,
                ax=ax)
    
    ax.set_ylim([-38, -28])
    ax.set_xlim([140, 155])
    
    fs_plot = sns.scatterplot(ax = ax0, data=fs_df, x='lon', y='lat', legend=False, zorder=3, s=scale**(1.5)*_size*5)
    
    australia.plot(ax = ax0, color='lightgrey', edgecolor='grey', linewidth=scale/3, zorder=1)
    
    #sns.scatterplot(ax = ax, data=client_locs, x='lon', y='lat', zorder=2, s=scale**(1.5)*_size*2, color='red')
    sns.kdeplot(data=client_locs, x='lon', y='lat', fill=True,
                cmap='coolwarm',
                alpha=0.2,
                #linewidth=0,
                levels=30, thresh=0.01,
                ax=ax0)
    
    ax0.set_ylim([y1, y2])
    ax0.set_xlim([x1, x2])
    plt.show()
    fig.get_figure().savefig("NSW_FS_client_KDE.png")
    print('Done!')
else:
    print('Plot already exists')
#%%Apply k-Means
#Test mode (less compute time) - only 100000 addresses
test_mode = False
use_abstract_clusters=False
cv=16

fraction_ids = list(range(cv))
if test_mode == True:
    client_locs_train = client_locs[['lon', 'lat']].sample(frac=1).sample(n=100000).to_numpy()
else:
    client_locs_train = client_locs[['lon', 'lat']].sample(frac=1).to_numpy()

if use_abstract_clusters==True:
    _n_clusters_init = int((client_locs_train.shape[0]**(0.5)+1)/50)
    _n_clusters_list = list(range(_n_clusters_init, _n_clusters_init*10, 25))
else:
    _n_clusters_list = list(range(fs_df.shape[0]-10, fs_df.shape[0]+10))

result_df = pd.DataFrame(columns=['data_fraction_ID', 'number_of_clients_fractured', 'number_of_clusters', 'silhouette_score', 'calinski_harabasz_score', 'davies_bouldin_score', 'cluster_center'])
print(f'N Clusters are {_n_clusters_list}')

#For Torch implementation
x = torch.from_numpy(client_locs_train)
if not os.path.isfile('df_k_means_metrics.csv'):
    print('='*80)
    print('Generating k-Means, this will last (~20 hours in production mode).')
    print('='*80)
    cores=multiprocessing.cpu_count()/2
    pool = multiprocessing.Pool(16)
    #result_df.loc[len(result_df)] = 
    result_df = pool.starmap(perform_k_means, list(itertools.product([client_locs_train], [cv], fraction_ids, _n_clusters_list)))
    pool.close()
    pool.join()
    result_df = pd.DataFrame(result_df)
    result_df.to_csv('df_k_means_metrics.csv')
    print('Done!')
else:
    print('Report already exists.')
    
#%%
#Plotting results
#Load fixed .csv dataframe
if os.path.isfile('df_k_means_metrics_fixed.csv'):
    predicted_plot = pd.read_csv('predicted_result_plot.csv')
    print(predicted_plot)
else:
    print('Launch df_analysis.ipynb to fix the database')
    input('Press any key to continue...')
    raise SystemExit(0)
fig1, (ax1, ax2) = plt.subplots(ncols = 2, figsize = _figsize*scale)
#Optional - plot existing fire stations
#fs_plot = sns.scatterplot(ax = ax1, data=fs_df, x='lon', y='lat', legend=False, zorder=3, s=scale**(1.5)*_size*10)
australia.plot(ax = ax1, color='lightgrey', edgecolor='grey', linewidth=scale/3, zorder=1)
fs_pred_plot = sns.scatterplot(ax = ax1, data=predicted_plot, x=predicted_plot['lon'], y=predicted_plot['lat'], legend=False, zorder=3, s=scale**(1.5)*_size*10, marker='x', color='red')
vor = Voronoi(predicted_plot[['lon', 'lat']])
voronoi_plot_2d(vor, ax=ax1, linewidth=scale/3)
'''#COLORIZE
for region in vor.regions:
    if not -1 in region:
        polygon = [vor.vertices[i] for i in region]
        plt.fill(*zip(*polygon), alpha=0.4)
'''
ax1.set_ylim([-38, -28])
ax1.set_xlim([140, 155])

australia.plot(ax = ax2, color='lightgrey', edgecolor='grey', linewidth=scale/3, zorder=1)
fs_pred_plot = sns.scatterplot(ax = ax2, data=predicted_plot, x=predicted_plot['lon'], y=predicted_plot['lat'], legend=False, zorder=3, s=scale**(1.5)*_size*10, marker='x', color='red')
vor = Voronoi(predicted_plot[['lon', 'lat']])
voronoi_plot_2d(vor, ax=ax2, linewidth=scale/3)

ax2.set_ylim([y1, y2])
ax2.set_xlim([x1, x2])
plt.show()
fig1.get_figure().savefig("NSW_FS_pred_Voronoi.png")

#%%
#Snippets
"""

for _n_clusters in _n_clusters_list:
    for fraction_id in fraction_ids:
        '''
        torch.cuda.empty_cache()
        reload(kmeans_pytorch)
        import kmeans_pytorchЫ
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
        '''
        #SKLearn implementation (comparison)
        #SKLearn is more precise - will use it anyway
        
        result_df.loc[len(result_df)] = perform_k_means(client_locs_train, cv, fraction_id, _n_clusters)
        
print('\nDF created:\n')
print(result_df.head(5))

#%%
result_df.to_csv('df_k_means_metrics.csv')

#%%
print(list(itertools.product([client_locs_train], [cv], fraction_ids, _n_clusters_list)))
"""
