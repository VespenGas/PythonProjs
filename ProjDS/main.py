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
import folium
from folium.plugins import HeatMap
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

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

if use_nsw_only==True:
    client_locs = client_locs[client_locs['region']=='NSW']
    

print('Dataframe example data:\n')
print(f'>There are {client_locs.shape[0]} clients in the area.\n')
print('Clients:\n')
print(client_locs.head(10))
print(f'>There are {fs_df.shape[0]} services in the area.\n')
print('\nServices:\n')
print(fs_df.head(10))
#%%
#Read GPD shapefile
print("\nExtracting shapefile (Australia)...\n")
assert os.path.isdir("AU_SPF"), 'No Australia shapefile found'

australia = gpd.read_file('AU_SPF/STE_2021_AUST_GDA2020.shp').set_index('STE_CODE21')
if use_nsw_only==True:
    australia = australia[australia['STE_NAME21']=='New South Wales']
australia = australia['geometry']

#print(australia.crs)
#print(australia.columns)

#%%
#Print Australia image + fire stations
print('\nPlotting...')
scale=6
_size=1

_figsize = np.asarray(matplotlib.rcParams['figure.figsize'])
sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=_figsize*scale)
fs_plot = sns.scatterplot(ax = ax, data=fs_df, x='lon', y='lat', legend=False, zorder=3, s=scale**(1.5)*_size*10)

australia.plot(ax = ax, color='lightgrey', edgecolor='grey', linewidth=scale/3, zorder=1)

#sns.scatterplot(ax = ax, data=client_locs, x='lon', y='lat', zorder=2, s=scale**(1.5)*_size*2, color='red')




