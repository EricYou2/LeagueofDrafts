import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#Import dataset and preprocessing
df = pd.read_csv('match_data/matches.csv')
df = df[df["win"] != -1]
X = df.drop(['win'], axis = 1)
y = df['win']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#Model
model = Sequential()
model.add(Dense(units=32, activation='relu', input_dim = len(X_train.columns)))
model.add(Dense(units=64, activation='relu'))
model.add(Dense(units=64, activation='relu'))
model.add(Dense(units=32, activation='relu'))
model.add(Dense(units=1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics='accuracy')

model.fit(X_train, y_train, epochs=3000, batch_size=128)

#Predictions
y_hat=model.predict(X_test)
y_hat = [0 if val<0.5 else 1 for val in y_hat]

print(accuracy_score(y_test, y_hat))

#Save model to load later
model.save("tfmodel")