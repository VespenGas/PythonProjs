#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#%%
import pandas as pd
import os
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
fs_df = parse_fs_php(php_contents, ['title', 'geo:lat', 'geo:long'])
fs_df[['geo:lat', 'geo:long']] = fs_df[['geo:lat', 'geo:long']].astype(float)
client_locs[['LON', 'LAT']] = client_locs[['LON', 'LAT']].astype(float)
fs_df[['geo:lat', 'geo:long']].round(6)
fs_df['title'] = fs_df['title'].str.rstrip(' Fire Station')
client_locs.columns = [x.lower() for x in client_locs.columns]
fs_df.rename(columns={'geo:lat' : 'lat', 'geo:long' : 'long'}, inplace=True)

print('Dataframe example data:\n')
print('Clients:\n')
print(client_locs.head(10))
print('\nServices:\n')
print(fs_df.head(10))


