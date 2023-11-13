#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 14:38:49 2023

@author: eugen
"""

import numpy as np
from numba import cuda, njit

@cuda.jit
def pairwise_distances(X, distances):
    i, j = cuda.grid(2)
    if i < X.shape[0] and j < X.shape[0]:
        diff = X[i] - X[j]
        distance = np.sqrt(np.sum(diff**2))
        distances[i, j] = distance

@njit(parallel=True)
def compute_silhouette(labels, distances):
    n = len(labels)
    a = np.zeros(n)
    b = np.zeros(n)
    s = np.zeros(n)

    for i in range(n):
        a[i] = np.mean(distances[i, labels == labels[i]])

    for i in range(n):
        b_min = np.inf
        for j in range(n):
            if labels[i] != labels[j]:
                b_val = np.mean(distances[i, labels == labels[j]])
                b_min = min(b_min, b_val)
        b[i] = b_min

    for i in range(n):
        s[i] = (b[i] - a[i]) / max(a[i], b[i])

    return np.mean(s)

def gpu_silhouette_score(X, labels):
    X = np.asarray(X)
    labels = np.asarray(labels)

    if X.shape[0] != labels.shape[0]:
        raise ValueError("Number of samples in X and labels must be the same.")

    threadsperblock = (16, 16)
    blockspergrid_x = int(np.ceil(X.shape[0] / threadsperblock[0]))
    blockspergrid_y = int(np.ceil(X.shape[0] / threadsperblock[1]))
    blockspergrid = (blockspergrid_x, blockspergrid_y)

    distances = np.zeros((X.shape[0], X.shape[0]))

    pairwise_distances[blockspergrid, threadsperblock](X, distances)
    silhouette = compute_silhouette(labels, distances)

    return silhouette
