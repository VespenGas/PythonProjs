#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pathlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score, homogeneity_score, completeness_score, v_measure_score
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
classes=[0,1,1,2,2,0]
#Perform vectorization
X = tfidf.fit_transform(list_of_texts)
#Reduce dimensionality with PCA
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(X.toarray())
#There are 3 clusters in the example data
num_clusters = 3
#k-Means
kmeans = KMeans(n_clusters=3, n_init=10)
kmeans.fit(X)

#Print all text file names (respective to text topic) and their designated cluster
print(list(zip(files, kmeans.labels_)))

print(f'Homogenuity score: {homogeneity_score(classes, kmeans.labels_)}')
print(f'Completeness score: {completeness_score(classes, kmeans.labels_)}')
print(f'V Measure score: {v_measure_score(classes, kmeans.labels_)}')
print('Additional metrics:')
print(f'Silhouette score = {silhouette_score(X, kmeans.labels_)}')
print(f'Calinski Harabasz score = {calinski_harabasz_score(np.asarray(X.todense()), kmeans.labels_)}')
print(f'Davies Bouldin score = {davies_bouldin_score(np.asarray(X.todense()), kmeans.labels_)}')

