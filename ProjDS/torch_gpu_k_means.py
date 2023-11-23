#!/usr/bin/env python3

import torch

device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

#X is input (2D matrix of coordinates [[lon, lat], ...])
#n_clusters is the number of clusters
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

cluster_centers, cluster_inference = kmeans_torch(X=x, k=n_clusters, device=device)
cluster_centers = cluster_centers.cpu().numpy()
cluster_inference = cluster_inference.cpu().numpy()

