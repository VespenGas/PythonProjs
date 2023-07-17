import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

np.set_printoptions(precision=3, suppress=True)

url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data' 
column_names = ['MPG', 'Cylinders', 'Displacement', 'Horsepower', 'Weight', 
                'Acceleration', 'Model Year', 'Origin'] 
 
raw_dataset = pd.read_csv(url, names=column_names, comment='\t', 
                          sep=' ', na_values='?', skipinitialspace=True)
dataset = raw_dataset.copy()
print(dataset.isna().sum())
dataset = dataset.dropna()

dataset['Origin'] = dataset['Origin'].map({1:'USA', 2: 'Europe', 3:'Japan'})
dataset = pd.get_dummies(dataset, columns=['Origin'], prefix='', prefix_sep='')

print(dataset)

#Perform test train split

train_dataset = dataset.sample(frac=0.8, random_state = 0)
test_dataset = dataset.drop(train_dataset.index)

#Data inspection

#sns.pairplot(train_dataset[['MPG', 'Cylinders', 'Displacement', 'Weight']], diag_kind='kde')
#plt.show()
#train_dataset.describe()

#Preprocessing

train_features = train_dataset.copy()
test_features  = test_dataset.copy()

train_labels = train_features.pop('MPG')
test_labels = test_features.pop('MPG')
#train_dataset.describe().transpose()[['mean', 'std']]

#Normalize

normalizer = layers.Normalization(axis=-1)
#^init normalizer
normalizer.adapt(np.array(train_features))
#^fits preprocessing layer state to the data
print(normalizer.mean.numpy())

#Linear Regression with 1 variable:
#Create a custom normalizer layer:
horsepower = np.array(train_features['Horsepower'])
horsepower_normalizer = layers.Normalization(input_shape=[1,], axis=None)
horsepower_normalizer.adapt(horsepower)
#Create a model with 2 layers: normalizer and Dense (linear transform)
#Sequential applies layers in sequence
horsepower_model = tf.keras.Sequential([
    horsepower_normalizer,
    layers.Dense(units=1)
    ])

print(horsepower_model.summary())
horsepower_model.compile(
    optimizer = keras.optimizers.legacy.Adam(learning_rate=0.1),
    loss='mean_absolute_error'
    )
history = horsepower_model.fit(
    train_features['Horsepower'],
    train_labels,
    epochs=100,
    verbose=0,
    validation_split=0.2
    )
hist = pd.DataFrame(history.history)
hist['epoch']=history.epoch
print(hist)
def plot_loss(history):
    plt.plot(history.history['loss'], label='Loss')
    plt.plot(history.history['val_loss'], label='Value Loss')
    plt.ylim([0,10])
    plt.xlabel('Epoch')
    plt.ylabel('Error [MPG]')
    plt.legend()
    plt.grid(True)
    plt.show()
plot_loss(history)
test_results = {}
test_results['horsepower_model'] = horsepower_model.evaluate(
    test_features['Horsepower'],
    test_labels,
    verbose=0
    )

#Prediction
x = tf.linspace(0.0, 250.0, 251)
y = horsepower_model.predict(x)
def plot_horsepower(x,y):
    plt.scatter(train_features['Horsepower'], train_labels, label='Data')
    plt.plot(x,y,color='k',label='Predictions')
    plt.ylabel('MPG')
    plt.xlabel('Horsepower')
    plt.legend()
    plt.show()
plot_horsepower(x, y)

#Linear regression with multiple variables

linear_model = tf.keras.Sequential([
    normalizer,
    layers.Dense(units=1)
    ])

#linear_model.predict(train_features)
linear_model.compile(
    optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=0.1),
    loss='mean_absolute_error'
    )
history2 = linear_model.fit(
    train_features,
    train_labels,
    epochs=100,
    validation_split=0.2,
    verbose=0
    )
plot_loss(history2)
test_results['linear_model'] = linear_model.evaluate(test_features, test_labels, verbose=0)






