#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 09:53:52 2023

@author: Evgeny Manturov
"""

from time import time
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import os, sys
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', 6)
def preprocess(df, column = 'text'):
    try:
        lemmatizer = WordNetLemmatizer()
        tokenizer = RegexpTokenizer(r'\w+')
    except:
        import nltk
        nltk.download('wordnet')
        nltk.download('punkt')
        print('NLTK token files downloaded, restart the script.', file=sys.stdout)
        raise SystemExit(0)
    df[column] = df[column].transform(lambda x: tokenizer.tokenize(x))
    df[column] = df[column].transform(lambda x: [lemmatizer.lemmatize(word).casefold() for word in x])
    df[column] = df[column].transform(lambda x: ' '.join(x))
    return df

def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x']+.02, point['y'], str(point['val']))
        
def find_model(train_file = 'train.csv'):
    t0 = time()
    assert os.path.isfile(train_file), f'{train_file} not found in CWD'
    df = pd.read_csv(train_file)
    df = preprocess(df).sample(frac=1)
    tfidf = TfidfVectorizer(sublinear_tf=True, max_df=0.5, min_df=5, ngram_range=(1,2),
                            stop_words='english', norm='l2', binary=False)
    train_df = df.iloc[0:int(len(df)*0.8)]
    test_df = df.iloc[int(len(df)*0.8):]
    emotions = df['emotion'].drop_duplicates()
    print(f'Emotions are:\n{emotions}')
    #emotion_dict = dict(zip(emotions, list(range(0, len(emotions)))))
    #emotion_dict_inverse = dict(zip(list(range(0, len(emotions))), emotions))
    X_train_raw = train_df[train_df.columns[0]]
    X_test_raw = test_df[test_df.columns[0]]
    y_train = train_df[train_df.columns[1]]
    y_test = test_df[test_df.columns[1]]
    X_train = tfidf.fit_transform(X_train_raw)
    X_test = tfidf.transform(X_test_raw)
    #print(tfidf.vocabulary_)
    features = tfidf.get_feature_names_out()
    print(f'\nFeature list: {features}\n')
    ttime=abs(time()-t0)
    print(f"Preprocessing time: {ttime} s")
    cv = 6
    scoring = 'f1_weighted'
    njobs = -2
    
    results = pd.DataFrame(columns=['Model', 'Best_Params', 'CV_Time', 'F1_score'])
    rf = RandomForestClassifier()
    svm = SVC()
    bayes = MultinomialNB()
    knn = KNeighborsClassifier()
    complement_bayes = ComplementNB()
    
    params_svm = {
        'C': [0.5, 1, 10, 30, 100],
        'gamma': [10, 1, 0.1, 0.01, 0.001, 0.0001],
        'kernel': ['rbf', 'linear'],
        }
    params_rf = {
        'criterion':['gini', 'entropy'],
        'n_estimators': [2000, 1000, 100, 50, 20],
        }
    params_knn = {
        'n_neighbors': [1, 3, 5, 7, 9],
        'weights': ['uniform', 'distance'],
        }
    params_bayes = {
        'force_alpha': [True, False]
        }
    params_complement_bayes = {
        'norm': [True, False]
        }
    
    t0 = time()
    print('='*80)
    print('SVM:')
    optimal_params_svm = GridSearchCV(svm, params_svm,
                                  cv=cv,
                                  scoring=scoring, verbose=0,
                                  n_jobs = njobs,
                                  refit=scoring
                                  )
    
    optimal_params_svm.fit(X_train, y_train)
    print(f'Best params: {optimal_params_svm.best_params_}')
    print(f'F1 Score: {optimal_params_svm.best_score_}')
    ttime = abs(time()-t0)
    print(f'Time taken: {ttime} s')
    results = pd.concat([results, pd.DataFrame([{'Model':'SVM', 'Best_Params':optimal_params_svm.best_params_, 'CV_Time':ttime, 'F1_score':optimal_params_svm.best_score_}])], ignore_index=True)
    
    t0 = time()
    print('='*80)
    print('Bayes:')
    optimal_params_bayes = GridSearchCV(bayes, params_bayes,
                                  cv=cv,
                                  scoring=scoring, verbose=0,
                                  n_jobs = njobs,
                                  refit=scoring
                                  )
    
    optimal_params_bayes.fit(X_train, y_train)
    print(f'Best params: {optimal_params_bayes.best_params_}')
    print(f'F1 Score: {optimal_params_bayes.best_score_}')
    ttime = abs(time()-t0)
    print(f'Time taken: {ttime} s')
    results = pd.concat([results, pd.DataFrame([{'Model':'Bayes', 'Best_Params':optimal_params_bayes.best_params_, 'CV_Time':ttime, 'F1_score':optimal_params_bayes.best_score_}])], ignore_index=True)
    
    t0 = time()
    print('='*80)
    print('Random Forests:')
    optimal_params_rf = GridSearchCV(rf, params_rf,
                                  cv=cv,
                                  scoring=scoring, verbose=0,
                                  n_jobs = njobs,
                                  refit=scoring
                                  )
    optimal_params_rf.fit(X_train, y_train)
    print(f'Best params: {optimal_params_rf.best_params_}')
    print(f'F1 Score: {optimal_params_rf.best_score_}')
    ttime = abs(time()-t0)
    print(f'Time taken: {ttime} s')
    results = pd.concat([results, pd.DataFrame([{'Model':'Random Forests', 'Best_Params':optimal_params_rf.best_params_, 'CV_Time':ttime, 'F1_score':optimal_params_rf.best_score_}])], ignore_index=True)
    
    t0 = time()
    print('='*80)
    print('kNN:')
    optimal_params_knn = GridSearchCV(knn, params_knn,
                                  cv=cv,
                                  scoring=scoring, verbose=0,
                                  n_jobs = njobs,
                                  refit=scoring
                                  )
    optimal_params_knn.fit(X_train, y_train)
    print(f'Best params: {optimal_params_knn.best_params_}')
    print(f'F1 Score: {optimal_params_knn.best_score_}')
    ttime = abs(time()-t0)
    print(f'Time taken: {ttime} s')
    results = pd.concat([results, pd.DataFrame([{'Model':'kNN', 'Best_Params':optimal_params_knn.best_params_, 'CV_Time':ttime, 'F1_score':optimal_params_knn.best_score_}])], ignore_index=True)
    
    t0 = time()
    print('='*80)
    print('Complement Bayes:')
    optimal_params_complement_bayes = GridSearchCV(complement_bayes, params_complement_bayes,
                                  cv=cv,
                                  scoring=scoring, verbose=0,
                                  n_jobs = njobs,
                                  refit=scoring
                                  )
    optimal_params_complement_bayes.fit(X_train, y_train)
    print(f'Best params: {optimal_params_complement_bayes.best_params_}')
    print(f'F1 Score: {optimal_params_complement_bayes.best_score_}')
    ttime = abs(time()-t0)
    print(f'Time taken: {ttime} s')
    results = pd.concat([results, pd.DataFrame([
        {'Model':'Complement Bayes', 'Best_Params':optimal_params_complement_bayes.best_params_, 'CV_Time':ttime, 'F1_score':optimal_params_complement_bayes.best_score_}])],
        ignore_index=True)
    
    results.sort_values('F1_score', ascending=False, inplace=True)
    print(results.head(5))
    plt.ylim([0,1])
    models_scatter = sns.scatterplot(results, x = results['CV_Time'], y = results['F1_score'])
    label_point(results['CV_Time'], results['F1_score'], results['Model'], plt.gca())
    plt.grid()
    models_scatter.get_figure().savefig('models_scatter.png', bbox_inches = 'tight')
    #Using the best model - Complement Bayes:
    model = ComplementNB(**optimal_params_complement_bayes.best_params_)
    t0 = time()
    predicted_set = model.fit(X_train, y_train).predict(X_test)
    ttime = t0 - time()
    print(f'Duration of final training and testing:{ttime}')
    
    side_compare = np.vstack((y_test.to_numpy(), predicted_set)).T
    out = pd.DataFrame({'text':X_test_raw, 'real':side_compare[:,0], 'pred':side_compare[:,1]})
    confusion = confusion_matrix(out['real'], out['pred'], labels=emotions)
    disp = ConfusionMatrixDisplay(confusion, display_labels=emotions)
    disp.plot()
    plt.xticks(rotation=45)
    plt.savefig('confusion_matrix.png', bbox_inches = 'tight')
    return results.iloc[0]
    #out['pred'].to_csv('predictions.txt', index=False, header=False)
def train_test(train_file = 'train.csv', test_file = 'test.csv'):
    assert os.path.isfile(train_file), 'Train file missing from dir'
    assert os.path.isfile(test_file), 'Test file missing from dir'
    t0 = time()
    train_df = pd.read_csv(train_file, index_col=False)
    test_df = pd.read_csv(test_file, index_col=False)
    train_df = preprocess(train_df)
    test_df = preprocess(test_df)
    tfidf = TfidfVectorizer(sublinear_tf=True, max_df=0.5, min_df=5, ngram_range=(1,2),
                            stop_words='english', norm='l2', binary=False)
    X_train = tfidf.fit_transform(train_df[train_df.columns[0]])
    X_test = tfidf.transform(test_df[test_df.columns[0]])
    y_train = train_df[train_df.columns[1]]
    ttime = abs(t0 - time())
    print(f'Preprocessing of train-test file: {ttime}s')
    t0 = time()
    model_selected = find_model('train_emotion.csv')
    ttime = abs(time()-t0)
    t0 = time()
    print(f'Total model selection time: {ttime}s')
    print(f'Model selected:\n{model_selected}')
    if model_selected['Model'] == 'SVM':
        model = SVC(**model_selected['Best_Params'])
    elif model_selected['Model'] == 'Complement Bayes':
        model = ComplementNB(**model_selected['Best_Params'])
    elif model_selected['Model'] == 'Random Forests':
        model = RandomForestClassifier(**model_selected['Best_Params'])
    elif model_selected['Model'] == 'Bayes':
        model = MultinomialNB(**model_selected['Best_Params'])
    elif model_selected['Model'] == 'kNN':
        model = KNeighborsClassifier(**model_selected['Best_Params'])
    else:
        print('Something is wrong - no model found!')
    pred = model.fit(X_train, y_train).predict(X_test)
    pred = pd.DataFrame(pred)
    pred.to_csv('predictions.txt', index=False, header=False)
    ttime = abs(t0 - time())
    print(f'Total model train and prediction time: {ttime}s')
    
    return 0
if __name__ == '__main__':
    train_test()



