#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.datasets import load_wine, load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score

def append_total_mean(*, df, scoring):
    filter_col = [col for col in df if col.startswith('mean')]
    df['total_mean'] = df[filter_col].sum(axis=1)/len(scoring)
    return df

wine_features, wine_labels = load_wine(return_X_y=True, as_frame=True)
iris_features, iris_labels = load_iris(return_X_y=True, as_frame=True)
'''
print(f'Wine features:\n {wine_features.head(5)}\n')
print(f'Wine labels:\n {wine_labels.head(5)}\n')
print(f'Iris features:\n {iris_features.head(5)}\n')
print(f'Iris labels:\n {iris_labels.head(5)}\n')
'''
#------------------------------------------------------------
wine_features_train, wine_features_test, wine_labels_train, wine_labels_test = train_test_split(wine_features, wine_labels, train_size=0.7, shuffle=True)
iris_features_train, iris_features_test, iris_labels_train, iris_labels_test = train_test_split(iris_features, iris_labels, train_size=0.7, shuffle=True)

scoring_str = ['accuracy', 'adjusted_mutual_info_score', 'adjusted_rand_score',
               'average_precision', 'balanced_accuracy', 'completeness_score',
               'explained_variance', 'f1', 'f1_macro', 'f1_micro', 'f1_samples',
               'f1_weighted', 'fowlkes_mallows_score', 'homogeneity_score',
               'jaccard', 'jaccard_macro', 'jaccard_micro', 'jaccard_samples',
               'jaccard_weighted', 'matthews_corrcoef', 'max_error', 
               'mutual_info_score', 'neg_brier_score', 'neg_log_loss', 
               'neg_mean_absolute_error', 'neg_mean_absolute_percentage_error', 
               'neg_mean_gamma_deviance', 'neg_mean_poisson_deviance', 
               'neg_mean_squared_error', 'neg_mean_squared_log_error', 
               'neg_median_absolute_error', 'neg_negative_likelihood_ratio', 
               'neg_root_mean_squared_error', 'normalized_mutual_info_score', 
               'positive_likelihood_ratio', 'precision', 'precision_macro', 
               'precision_micro', 'precision_samples', 'precision_weighted', 
               'r2', 'rand_score', 'recall', 'recall_macro', 'recall_micro', 
               'recall_samples', 'recall_weighted', 'roc_auc', 'roc_auc_ovo', 
               'roc_auc_ovo_weighted', 'roc_auc_ovr', 'roc_auc_ovr_weighted',
               'top_k_accuracy', 'v_measure_score'] #to check which strings are available

#------------------------------------------------------------------------------
#SETUP PARAMETERS HERE
param_grid_svm = [
    {'C':[0.5, 1, 10, 30, 100],
     'gamma': [10, 1, 0.1, 0.01, 0.001, 0.0001],
     'kernel': ['rbf', 'linear']}
    ]
param_grid_knn = [
    {'n_neighbors': [1, 3, 5, 7, 9],
     'weights': ['uniform', 'distance']}
    ]
display_top = 5
_scoring = ['accuracy', 'recall_weighted', 'f1_weighted', 'precision_micro']
#Here it is important to mention that changing "precision_micro" to any other 
#"precision" metric will flood the console with ill-placed metric warnings

_cv = 10 #num of cross-validations

#------------------------------------------------------------------------------
optimal_params_wine_svc = GridSearchCV(svm.SVC(), param_grid_svm,
                              cv=_cv,
                              scoring=_scoring, verbose=0,
                              n_jobs = -1,
                              refit=False
                              )
optimal_params_iris_svc = GridSearchCV(svm.SVC(), param_grid_svm,
                              cv=_cv,
                              scoring=_scoring, verbose=0,
                              n_jobs = -1,
                              refit=False
                              )
optimal_params_wine_knn = GridSearchCV(KNeighborsClassifier(), param_grid_knn,
                              cv=_cv,
                              scoring=_scoring, verbose=0,
                              n_jobs = -1,
                              refit=False
                              )
optimal_params_iris_knn = GridSearchCV(KNeighborsClassifier(), param_grid_knn,
                              cv=_cv,
                              scoring=_scoring, verbose=0,
                              n_jobs = -1,
                              refit=False
                              )

optimal_params_wine_svc.fit(wine_features_train, wine_labels_train)
optimal_params_iris_svc.fit(iris_features_train, iris_labels_train)
optimal_params_wine_knn.fit(wine_features_train, wine_labels_train)
optimal_params_iris_knn.fit(iris_features_train, iris_labels_train)

df = pd.DataFrame(optimal_params_wine_svc.cv_results_)
filter_col = [col for col in df if col.startswith('mean')]

svc_list_of_cols = ['param_C', 'param_kernel', 'param_gamma']
svc_list_of_cols.extend(filter_col)
knn_list_of_cols = ['param_n_neighbors', 'param_weights']
knn_list_of_cols.extend(filter_col)

param_wine_svc = pd.DataFrame(optimal_params_wine_svc.cv_results_)[svc_list_of_cols]
param_wine_svc = append_total_mean(df = param_wine_svc, scoring = _scoring).sort_values(by=['total_mean'], ascending=False).head(display_top)

param_iris_svc = pd.DataFrame(optimal_params_iris_svc.cv_results_)[svc_list_of_cols]
param_iris_svc = append_total_mean(df = param_iris_svc, scoring = _scoring).sort_values(by=['total_mean'], ascending=False).head(display_top)

param_wine_knn = pd.DataFrame(optimal_params_wine_knn.cv_results_)[knn_list_of_cols]
param_wine_knn = append_total_mean(df = param_wine_knn, scoring = _scoring).sort_values(by=['total_mean'], ascending=False).head(display_top)

param_iris_knn = pd.DataFrame(optimal_params_iris_knn.cv_results_)[knn_list_of_cols]
param_iris_knn = append_total_mean(df = param_iris_knn, scoring = _scoring).sort_values(by=['total_mean'], ascending=False).head(display_top)

print('\nGrid search Cross-Validation for WINE dataset (SVC):\n')
print(param_wine_svc)
print('\nGrid search Cross-Validation for IRIS dataset (SVC):\n')
print(param_iris_svc)
print('\nGrid search Cross-Validation for WINE dataset (kNN):\n')
print(param_wine_knn)
print('\nGrid search Cross-Validation for IRIS dataset (kNN):\n')
print(param_iris_knn)
#-----------------------------------------------------------------------------
print('='*80)
print('Determining best model')
print('For WINE:')
print(f"SVC max score: {param_wine_svc.iloc[0]['total_mean']}\n with C = {param_wine_svc.iloc[0]['param_C']}, gamma = {param_wine_svc.iloc[0]['param_gamma']} and kernel = {param_wine_svc.iloc[0]['param_kernel']}")
print(f"kNN max score: {param_wine_knn.iloc[0]['total_mean']}\n with num of neighbors = {param_wine_knn.iloc[0]['param_n_neighbors']} and kernel = {param_wine_knn.iloc[0]['param_weights']}")
if param_wine_svc.iloc[0]['total_mean'] > param_wine_knn.iloc[0]['total_mean']:
    print('SVC picked for WINE:\n')
    wine_c = param_wine_svc.iloc[0]['param_C']
    wine_gamma = param_wine_svc.iloc[0]['param_gamma']
    wine_kernel = param_wine_svc.iloc[0]['param_kernel']
    model_wine=svm.SVC(C = wine_c, kernel = wine_kernel, gamma = wine_gamma)
    model_wine.fit(wine_features_train, wine_labels_train)
    pred_wine = model_wine.predict(wine_features_test)
    print(f'Accuracy: {accuracy_score(wine_labels_test, pred_wine)}')
    print(f'Recall: {recall_score(wine_labels_test, pred_wine, average="weighted")}')
    print(f'F1: {f1_score(wine_labels_test, pred_wine, average="weighted")}')
    print(f'Precision: {precision_score(wine_labels_test, pred_wine, average="weighted")}')
    print('\n')
else:
    print('kNN picked for WINE:\n')
    wine_n_neighbors = param_wine_knn.iloc[0]['param_n_neighbors']
    wine_weights = param_wine_knn.iloc[0]['param_weights']
    model_wine=KNeighborsClassifier(n_neighbors = wine_n_neighbors, weights = wine_weights)
    model_wine.fit(wine_features_train, wine_labels_train)
    pred_wine = model_wine.predict(wine_features_test)
    print(f'Accuracy: {accuracy_score(wine_labels_test, pred_wine)}')
    print(f'Recall: {recall_score(wine_labels_test, pred_wine, average="weighted")}')
    print(f'F1: {f1_score(wine_labels_test, pred_wine, average="weighted")}')
    print(f'Precision: {precision_score(wine_labels_test, pred_wine, average="weighted")}')
    print('\n')
print('For IRIS:')
print(f"SVC max score: {param_iris_svc.iloc[0]['total_mean']}\n with C = {param_iris_svc.iloc[0]['param_C']}, gamma = {param_iris_svc.iloc[0]['param_gamma']} and kernel = {param_iris_svc.iloc[0]['param_kernel']}")
print(f"kNN max score: {param_iris_knn.iloc[0]['total_mean']}\n with num of neighbors = {param_iris_knn.iloc[0]['param_n_neighbors']} and kernel = {param_iris_knn.iloc[0]['param_weights']}")
if param_iris_svc.iloc[0]['total_mean'] > param_iris_knn.iloc[0]['total_mean']:
    print('SVC picked for IRIS:\n')
    iris_c = param_iris_svc.iloc[0]['param_C']
    iris_gamma = param_iris_svc.iloc[0]['param_gamma']
    iris_kernel = param_iris_svc.iloc[0]['param_kernel']
    model_iris=svm.SVC(C = iris_c, kernel = iris_kernel, gamma = iris_gamma)
    model_iris.fit(iris_features_train, iris_labels_train)
    pred_iris = model_iris.predict(iris_features_test)
    print(f'Accuracy: {accuracy_score(iris_labels_test, pred_iris)}')
    print(f'Recall: {recall_score(iris_labels_test, pred_iris, average="weighted")}')
    print(f'F1: {f1_score(iris_labels_test, pred_iris, average="weighted")}')
    print(f'Precision: {precision_score(iris_labels_test, pred_iris, average="weighted")}')
    print('\n')
else:
    print('kNN picked for IRIS:\n')
    iris_n_neighbors = param_iris_knn.iloc[0]['param_n_neighbors']
    iris_weights = param_iris_knn.iloc[0]['param_weights']
    model_iris=KNeighborsClassifier(n_neighbors = iris_n_neighbors, weights = iris_weights)
    model_iris.fit(iris_features_train, iris_labels_train)
    pred_iris = model_iris.predict(iris_features_test)
    print(f'Accuracy: {accuracy_score(iris_labels_test, pred_iris)}')
    print(f'Recall: {recall_score(iris_labels_test, pred_iris, average="weighted")}')
    print(f'F1: {f1_score(iris_labels_test, pred_iris, average="weighted")}')
    print(f'Precision: {precision_score(iris_labels_test, pred_iris, average="weighted")}')
    print('\n')

