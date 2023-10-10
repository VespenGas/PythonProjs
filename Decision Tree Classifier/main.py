#!/usr/bin/env python
# coding: utf-8

# In[1]:

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_wine


# In[2]:


wine_df_features, wine_df_labels = load_wine(as_frame = True).data, load_wine(as_frame = True).target


# In[3]:


wine_df_features_train, wine_df_features_test, wine_df_labels_train, wine_df_labels_test = train_test_split(wine_df_features, wine_df_labels, test_size = 0.3, random_state = 0)


# In[4]:


wine_df_features_train


# In[5]:


wine_df_labels_train


# In[6]:


model = DecisionTreeClassifier(criterion = "entropy", random_state = 0)
#options: “gini”, “entropy”, “log_loss”


# In[7]:


model.fit(wine_df_features_train, wine_df_labels_train)


# In[8]:


wine_df_labels_predicted = model.predict(wine_df_features_test)


# In[9]:


print(wine_df_labels_predicted)


# In[10]:


print(wine_df_labels_test.to_numpy())


# In[11]:


print(f'Accuracy score is: {accuracy_score(wine_df_labels_predicted, wine_df_labels_test.to_numpy())}')
#With random_state = 0 everywhere in sklearn:
#0.9444444444444444 for GINI
#0.9444444444444444 for entropy
#0.9444444444444444 for log_loss - equivalent


# In[ ]:




