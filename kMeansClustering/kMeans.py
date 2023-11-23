#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pathlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score, homogeneity_score, completeness_score, v_measure_score
import seaborn as sns
#Vectorizer
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=0.1, max_df=0.5, ngram_range=(1,2),
                        stop_words='english', norm='l2', binary=False,
                        strip_accents='unicode')
#Open all texts
files = list(pathlib.Path().glob('*.txt'))
files = [str(file) for file in files]
files.sort()
list_of_texts = []
for file in files:
    with open(file, 'r') as f:
        list_of_texts.append(f.read())
#Based on contents, the classes are:
    '''\
        0 - military airctraft-related (wikipedia)
        1 - The Forgotten Realms-related (wikipedia)
        2 - electrical engineering-related (wikipedia)
        '''
classes=[0,1,1,2,2,0] #for common metrics
#Perform vectorization
X = tfidf.fit_transform(list_of_texts)
#Reduce dimensionality with PCA
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(X.toarray())
#There are 3 clusters in the example data
n_clusters_list = list(range(2, 5, 1))
#k-Means
print(reduced_data)
for n_clusters in n_clusters_list:
    kmeans = KMeans(n_clusters=n_clusters, n_init=10)
    kmeans.fit(reduced_data)
    
    #Print all text file names (respective to text topic) and their designated cluster
    print(f'Number of clusters: {n_clusters}')
    print(list(zip(files, kmeans.labels_)))
    if n_clusters==3:
        sns.scatterplot(data=reduced_data, x=reduced_data[:,0], y=reduced_data[:,1], hue=kmeans.labels_)
    print(f'Homogenuity score: {homogeneity_score(classes, kmeans.labels_)}')
    print(f'Completeness score: {completeness_score(classes, kmeans.labels_)}')
    print(f'V Measure score: {v_measure_score(classes, kmeans.labels_)}')
    print('Additional metrics:')
    print(f'Silhouette score = {silhouette_score(X, kmeans.labels_)}')
    print(f'Calinski Harabasz score = {calinski_harabasz_score(np.asarray(X.todense()), kmeans.labels_)}')
    print(f'Davies Bouldin score = {davies_bouldin_score(np.asarray(X.todense()), kmeans.labels_)}')

