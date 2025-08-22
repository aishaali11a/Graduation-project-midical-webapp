import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import uniform, choice, normal
from sklearn.preprocessing import StandardScaler
import tensorflow
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay
import joblib

# Step 1: Load the data from csv file
dataset = pd.read_csv('disease_diagnosis.csv')
dataset.info()
dataset.describe()

dataset['Gender'] = dataset['Gender'].str.strip().str.lower().replace({'female': 0, 'male': 1})

columns = ["Age","Gender","Heart_Rate_bpm","Body_Temperature_C","Blood_Pressure_mmHg","Oxygen_Saturation_%"]
X = dataset[columns].values # Features
Y = dataset['Diagnosis'].values

#diagnosis = ["Flu","Healthy","Bronchitis","Cold","Pneumonia"]
#symptoms = ["Body ache","Cough","Fatigue","Fever","Headache","Runny nose","Shortness of breath","Sore throat"]

l_encode = LabelEncoder()
l_encode.fit(Y)
Y = l_encode.transform(Y)

# Step 3: Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=1) # 70% training and 30% test


# ----------------------
# Support Vector Machine
# ----------------------
from sklearn.svm import SVC

# Step 5: Create the SVM model
model = SVC(kernel='linear')  # You can change the kernel to 'rbf', 'poly', etc.

# Step 6: Train the model
model.fit(X_train, y_train)

# Step 7: Make predictions
predictions = model.predict(X_test)

# Step 8: Generate the confusion matrix
cm = confusion_matrix(y_test, predictions)

# Step 9: Display the confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0, 1, 2, 3, 4,])
disp.plot(cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.show()

# Step 10: Generate the classification report
report = classification_report(y_test, predictions)
print(report)

